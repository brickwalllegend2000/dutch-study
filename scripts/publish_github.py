#!/usr/bin/env python3
"""Publish this prepared vault to a PRIVATE GitHub repository using your gh login.

Run: python scripts/publish_github.py
Requires Git, GitHub CLI, and an authenticated account allowed to create/write the repo.
Does not request, read or print token values. Existing unrelated repositories are rejected.
"""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
from library import ROOT, validate


def command(args, *, check=True, input_text=None):
    result=subprocess.run(args,cwd=ROOT,text=True,input=input_text,capture_output=True)
    if check and result.returncode:
        raise RuntimeError(f'{args[0]} {args[1]} failed: {result.stderr.strip() or result.stdout.strip()}')
    return result


def gh_json(args):
    result=command(['gh']+args)
    return json.loads(result.stdout) if result.stdout.strip() else None


def check_destination(metadata, matching_library):
    if not metadata.get('isPrivate'): raise ValueError('Destination must be private before any study data is uploaded.')
    if not metadata.get('isEmpty') and not matching_library:
        raise ValueError('Refusing to upload into a nonempty unrelated repository. Use an empty private repository.')


def ensure_repository(repo):
    result=command(['gh','repo','view',repo,'--json','nameWithOwner,isPrivate,isEmpty,url'],check=False)
    if result.returncode:
        # An access error is allowed to fail clearly; do not switch identity or make a public repo.
        command(['gh','repo','create',repo,'--private','--description','Canonical Dutch study library and Obsidian vault'])
        metadata=gh_json(['repo','view',repo,'--json','nameWithOwner,isPrivate,isEmpty,url'])
    else: metadata=json.loads(result.stdout)
    matching=False
    if not metadata.get('isEmpty'):
        marker=command(['gh','api',f'repos/{repo}/contents/sources/import-summary.json','--jq','.path'],check=False)
        matching=marker.returncode==0 and marker.stdout.strip()=='sources/import-summary.json'
    check_destination(metadata,matching)
    return metadata


def check_remote_urls(repo, fetch_url, push_urls):
    expected=f'https://github.com/{repo}.git'
    allowed={expected,expected.removesuffix('.git'),f'git@github.com:{repo}.git'}
    if fetch_url not in allowed: raise ValueError('origin points to another repository; no remote was changed.')
    if not push_urls or any(url not in allowed for url in push_urls):
        raise ValueError('origin has an unchecked push destination; remove or correct its push URLs before publishing.')


def prepare_git(repo):
    expected=f'https://github.com/{repo}.git'
    if not (ROOT/'.git').exists(): command(['git','init','-b','main'])
    branch=command(['git','branch','--show-current']).stdout.strip()
    if branch not in ('main','setup'):
        raise ValueError(f'Current branch is {branch!r}; switch to main or the initial setup branch before publishing.')
    if branch=='setup': command(['git','branch','-m','main'])
    remote=command(['git','remote','get-url','origin'],check=False)
    if remote.returncode: command(['git','remote','add','origin',expected])
    fetch_url=command(['git','remote','get-url','origin']).stdout.strip()
    push_urls=command(['git','remote','get-url','--push','--all','origin']).stdout.splitlines()
    check_remote_urls(repo,fetch_url,push_urls)
    # Scope credential helper to this clone, leaving global user settings unchanged.
    command(['git','config','--local','credential.https://github.com.helper',''])
    command(['git','config','--local','--add','credential.https://github.com.helper','!gh auth git-credential'])
    if command(['git','var','GIT_AUTHOR_IDENT'],check=False).returncode:
        profile=gh_json(['api','user'])
        command(['git','config','--local','user.name',profile.get('name') or profile['login']])
        command(['git','config','--local','user.email',f'{profile["id"]}+{profile["login"]}@users.noreply.github.com'])
    command(['git','add','.'])
    if command(['git','diff','--cached','--quiet'],check=False).returncode:
        command(['git','commit','-m','feat: configure canonical Dutch study library and Obsidian vault'])
    command(['git','push','-u','origin','main']) # Fast-forward only; never force.


def configure_tracking(repo):
    config=json.loads((ROOT/'.github/bootstrap.json').read_text())
    command(['gh','repo','edit',repo,'--enable-issues','--enable-projects','--delete-branch-on-merge','--enable-wiki=false'])
    for label in config['labels']:
        command(['gh','label','create',label['name'],'--repo',repo,'--color',label['color'],'--description',label['description'],'--force'])
    milestones=gh_json(['api',f'repos/{repo}/milestones?state=all&per_page=100'])
    milestone_map={m['title']:m['number'] for m in milestones}
    for item in config['milestones']:
        if item['title'] not in milestone_map:
            m=gh_json(['api',f'repos/{repo}/milestones','-X','POST','-f',f'title={item["title"]}','-f',f'description={item["description"]}'])
            milestone_map[item['title']]=m['number']
    existing=gh_json(['issue','list','--repo',repo,'--state','all','--limit','1000','--json','number,title,url'])
    issue_map={i['title']:i for i in existing}
    for item in config['issues']:
        if item['title'] not in issue_map:
            payload={'title':item['title'],'body':item['body'],'labels':item['labels'],'milestone':milestone_map[item['milestone']]}
            result=command(['gh','api',f'repos/{repo}/issues','-X','POST','--input','-'],input_text=json.dumps(payload))
            i=json.loads(result.stdout);issue_map[item['title']]={'number':i['number'],'title':i['title'],'url':i['html_url']}
    return [issue_map[i['title']] for i in config['issues']]


def configure_project(repo,issues):
    owner=repo.split('/')[0];title='Dutch study'
    existing=gh_json(['project','list','--owner',owner,'--format','json','--limit','100'])
    project=next((p for p in existing.get('projects',[]) if p.get('title')==title and not p.get('closed')),None)
    if project is None: project=gh_json(['project','create','--owner',owner,'--title',title,'--format','json'])
    number=str(project['number'])
    command(['gh','project','link',number,'--owner',owner,'--repo',repo])
    for issue in issues: command(['gh','project','item-add',number,'--owner',owner,'--url',issue['url']])
    # GitHub creates its normal Todo / In Progress / Done status field. Review is an issue label.
    return project.get('url',f'https://github.com/users/{owner}/projects/{number}')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',default='brickwalllegend2000/dutch-study',help='Private destination in owner/name form')
    parser.add_argument('--skip-project',action='store_true',help='Use issue labels and searches without a Project board')
    args=parser.parse_args()
    import re
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',args.repo): parser.error('--repo must be owner/name')
    if args.repo!='brickwalllegend2000/dutch-study': parser.error('This package is configured for brickwalllegend2000/dutch-study. Update repository links in the package before selecting another destination.')
    for binary in ('git','gh'):
        if not shutil.which(binary): raise SystemExit(f'Install {binary} first, then rerun. See docs/PUBLISH.md.')
    command(['gh','auth','status'])
    errors=validate()
    if errors: raise ValueError('Local validation failed:\n'+'\n'.join(errors))
    command([sys.executable,'-m','unittest','discover','-s','tests','-v'])
    metadata=ensure_repository(args.repo)
    prepare_git(args.repo)
    issues=configure_tracking(args.repo)
    project_url=None;warnings=[]
    if not args.skip_project:
        try:project_url=configure_project(args.repo,issues)
        except RuntimeError as e:warnings.append('Project board could not be configured: '+str(e))
    report={'repository':metadata['url'],'private':True,'issues':issues,'project':project_url,'warnings':warnings,'actions':'https://github.com/'+args.repo+'/actions'}
    (ROOT/'docs/publishing-result.json').write_text(json.dumps(report,indent=2)+'\n')
    command(['git','add','docs/publishing-result.json'])
    if command(['git','diff','--cached','--quiet'],check=False).returncode:
        command(['git','commit','-m','docs: record published repository and task links'])
        check_remote_urls(args.repo, command(['git','remote','get-url','origin']).stdout.strip(), command(['git','remote','get-url','--push','--all','origin']).stdout.splitlines())
        command(['git','push','origin','main'])
    print(json.dumps(report,indent=2))
    print('Repository and tasks published. Open the clone folder as an existing vault in Obsidian. Check Actions for remote verification.')
    return 0

if __name__=='__main__':
    try:sys.exit(main())
    except (RuntimeError,ValueError) as e:print(str(e),file=sys.stderr);sys.exit(1)
