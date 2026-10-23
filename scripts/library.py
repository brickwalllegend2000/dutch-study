#!/usr/bin/env python3
"""Search, render and validate the Dutch library; Python standard library only."""
import argparse
import csv
import hashlib
import html
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
VIEWS = 'wiki/vocabulary'
FIELDS = ['id','dutch','english','article','word_type','forms','auxiliary','participle','examples','chapters','categories','notes','source_ids','occurrence_ids','review_status','reviewed_on']


def plain(value):
    value = re.sub(r'<br\s*/?>', ' ', value, flags=re.I)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', value))).strip()


class TableParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tables=[]; self.table=None; self.row=None; self.cell=None
    def handle_starttag(self, tag, attrs):
        if tag=='table': self.table=[]
        elif tag=='tr' and self.table is not None: self.row=[]
        elif tag in ('td','th') and self.row is not None: self.cell=[]
        elif tag=='br' and self.cell is not None: self.cell.append(' ')
    def handle_data(self, data):
        if self.cell is not None: self.cell.append(data)
    def handle_endtag(self, tag):
        if tag in ('td','th') and self.cell is not None:
            self.row.append(re.sub(r'\s+',' ',''.join(self.cell)).strip()); self.cell=None
        elif tag=='tr' and self.row is not None:
            self.table.append(self.row); self.row=None
        elif tag=='table' and self.table is not None:
            self.tables.append(self.table); self.table=None


def markdown_cells(line):
    return [plain(x.replace('\\|','|')) for x in re.split(r'(?<!\\)\|',line.strip().strip('|'))]


def parse_tables(text):
    """Return tables in source order, including enhanced Notion HTML tables."""
    parts=[]
    for m in re.finditer(r'<table\b[^>]*>.*?</table>|(?:^\s*\|[^\n]*\n?)+', text, re.S|re.M):
        block=m.group()
        if block.lstrip().startswith('<table'):
            parser=TableParser(); parser.feed(block); parts.extend(parser.tables)
        else:
            rows=[markdown_cells(line) for line in block.splitlines() if line.strip().startswith('|')]
            parts.append([row for row in rows if not all(re.fullmatch(r'[:\-\s]+',c) for c in row)])
    return parts


def normalized(term):
    return re.sub(r'\s+',' ',unicodedata.normalize('NFC',term)).strip().casefold()


def record_id(term):
    return 'VOC-' + hashlib.sha256(normalized(term).encode()).hexdigest()[:12]


def consolidate(occurrences):
    """Group exact normalized terms only; preserve variants and all source locators."""
    groups={}
    for o in occurrences:
        term=o.get('dutch','').strip()
        if not term: continue
        key=normalized(term)
        groups.setdefault(key,[]).append(o)
    rows=[]
    for key, items in sorted(groups.items()):
        row={f:'' for f in FIELDS}; row['id']=record_id(key); row['dutch']=items[0]['dutch'].strip()
        for field in FIELDS[2:12]:
            vals=sorted({str(o.get(field,'')).strip() for o in items} - {'','–','—','-'})
            row[field]=(';' if field in ('chapters','categories') else ' ⟐ ').join(vals)
        row['source_ids']=';'.join(sorted({o['source_id'] for o in items if o.get('source_id')}))
        row['occurrence_ids']=';'.join(sorted({o['occurrence_id'] for o in items if o.get('occurrence_id')}))
        row['review_status']='needs-review'
        rows.append(row)
    return rows


def table_md(table):
    if not table: return ''
    width=max(map(len,table))
    def line(row):
        cells=[c.replace('|','\\|').replace('\n','<br>') for c in row]
        return '| '+' | '.join(cells+['']*(width-len(cells)))+' |'
    return '\n'+line(table[0])+'\n'+line(['---']*width)+'\n'+'\n'.join(line(r) for r in table[1:])+'\n'


def to_markdown(text, mapping, current_path):
    def local_link(url, label=''):
        match=re.search(r'([a-f0-9]{32})(?:[?/#]|$)',url)
        if match and match[1] in mapping:
            dest,title=mapping[match[1]]
            url=Path(os.path.relpath(dest,Path(current_path).parent)).as_posix()
            label=label or title
        return '['+(plain(label) or 'Source')+']('+url+')'
    def table_replace(m):
        p=TableParser(); p.feed(m[0]); return table_md(p.tables[0]) if p.tables else m[0]
    text=re.sub(r'<table\b[^>]*>.*?</table>',table_replace,text,flags=re.S)
    text=re.sub(r'<(?:mention|page)\b[^>]*url="([^"]+)"[^>]*>(.*?)</(?:mention|page)>',lambda m:local_link(m[1],m[2]),text,flags=re.S)
    text=re.sub(r'<mention\b[^>]*url="([^"]+)"[^>]*/>',lambda m:local_link(m[1]),text)
    text=re.sub(r'<database\b[^>]*url="([^"]+)"[^>]*>(.*?)</database>',lambda m:local_link(m[1],m[2] or 'Original Notion database'),text,flags=re.S)
    text=re.sub(r'<image\s+source="([^"]+)"[^>]*(?:/>|>(.*?)</image>)',lambda m:'\n[Source image reference]('+m[1]+')\n'+(m[2] or ''),text,flags=re.S)
    text=re.sub(r'<(b|strong)>(.*?)</\1>',r'**\2**',text,flags=re.S)
    text=re.sub(r'<(i|em)>(.*?)</\1>',r'*\2*',text,flags=re.S)
    text=re.sub(r'<code>(.*?)</code>',r'`\1`',text,flags=re.S)
    text=re.sub(r'<br\s*/?>','\n',text)
    text=re.sub(r'<table-of-contents\s*/>','',text)
    text=re.sub(r'<date\s+start="([^"]+)"[^>]*/>',r'\1',text)
    text=re.sub(r'</?(?:columns|column|callout|toggle|quote|p)\b[^>]*>','\n',text)
    # Imported plain Markdown links may also target Notion pages.
    text=re.sub(r'\[([^\]]+)\]\((https://app\.notion\.com/[^\s)]+)\)',lambda m:local_link(m[2],m[1]),text)
    return re.sub(r'\n{3,}','\n\n',html.unescape(text)).strip()+'\n'


def read_rows(root=ROOT):
    with (root/'vocabulary.csv').open(encoding='utf-8',newline='') as f:
        reader=csv.DictReader(f)
        if reader.fieldnames!=FIELDS: raise ValueError('vocabulary.csv schema differs from documented FIELDS')
        return list(reader)


def validate_rows(rows, source_ids):
    errors=[]; ids=set()
    for n,row in enumerate(rows,2):
        rid=row.get('id','')
        if rid in ids: errors.append(f'row {n}: duplicate id {rid}')
        ids.add(rid)
        if not re.fullmatch(r'VOC-[a-f0-9]{12}',rid): errors.append(f'row {n}: invalid id')
        if not row.get('dutch','').strip(): errors.append(f'row {n}: empty Dutch term')
        if row.get('review_status') not in ('needs-review','reviewed'): errors.append(f'row {n}: invalid review status')
        if row.get('review_status')=='reviewed' and not re.fullmatch(r'\d{4}-\d{2}-\d{2}',row.get('reviewed_on','')): errors.append(f'row {n}: reviewed date required')
        sources=row.get('source_ids','').split(';')
        if not all(sources): errors.append(f'row {n}: source required')
        for source in sources:
            if source not in source_ids: errors.append(f'row {n}: unknown source {source}')
        if any(x and x not in {str(i) for i in range(1,9)} for x in row.get('chapters','').split(';')): errors.append(f'row {n}: invalid chapter')
    return errors


def rendered(root=ROOT):
    rows=read_rows(root); pages={}; index=['# Vocabulary','', '> Generated from [vocabulary.csv](../../vocabulary.csv). Edit the CSV, then run `python scripts/library.py build`.','']
    def listing(selected):
        result=['| Dutch | English | Review |','| --- | --- | --- |']
        for r in selected:
            dutch=r['dutch'].replace('|','\\|').replace('\n','<br>'); english=r['english'].replace('|','\\|').replace('\n','<br>')
            result.append(f"| [{dutch}](words/{r['id']}.md) | {english} | {r['review_status']} |")
        return '\n'.join(result)+'\n'
    for r in rows:
        lines=['---',f"id: {r['id']}",f"title: {json.dumps(r['dutch'],ensure_ascii=False)}",'generated: true',f"review_status: {r['review_status']}",'---',f"# {r['dutch']}",'', '> Generated reading view. Edit the matching row in [vocabulary.csv](../../../vocabulary.csv).','']
        for field in FIELDS[2:12]:
            if r[field]: lines += ['## '+field.replace('_',' ').title(),'',r[field],'']
        lines+=['## Sources','']+[f'- [{sid}](../../../sources/pages/{sid}.md)' for sid in r['source_ids'].split(';')]
        lines+=['', 'Original source occurrences: [provenance ledger](../../../sources/vocabulary-occurrences.json).', '', '[All vocabulary](../VOCABULARY.md) · [Home](../../../README.md)','']
        pages[f"{VIEWS}/words/{r['id']}.md"]='\n'.join(lines)
    pages[f'{VIEWS}/VOCABULARY.md']='\n'.join(index)+listing(rows)
    pages[f'{VIEWS}/PERFECTUM.md']='# Perfectum verbs\n\n> Generated; auxiliary variants retain source context. Review the source occurrences before generalizing.\n\n'+listing([r for r in rows if r['participle']])
    pages[f'{VIEWS}/IRREGULAR-VERBS.md']='# Irregular verbs\n\n'+listing([r for r in rows if 'Irregular verbs' in r['categories'].split(';')])
    pages[f'{VIEWS}/PERFECTUM-STUDY-LIST.md']='# Perfectum study list — 80 verbs\n\n[Source transcription and usage notes](../../sources/pages/401f89e5e0fc80f29352c76d2b8204b7.md)\n\n'+listing([r for r in rows if 'Perfectum study list' in r['categories'].split(';')])
    pages[f'{VIEWS}/NEEDS-REVIEW.md']='# Vocabulary needing review\n\n'+listing([r for r in rows if r['review_status']=='needs-review'])
    for n in range(1,9):
        pages[f'{VIEWS}/CHAPTER-{n:02}.md']=f'# Chapter {n} vocabulary\n\n[Chapter {n} guide](../../course/chapter-{n:02}.md) · [All vocabulary](VOCABULARY.md)\n\n'+listing([r for r in rows if str(n) in r['chapters'].split(';')])
    return pages


def build(root=ROOT):
    expected=rendered(root)
    for name,body in expected.items():
        path=root/name; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(body,encoding='utf-8')
    # Remove obsolete generated word views only, never user-authored notes.
    for p in (root/VIEWS/'words').glob('VOC-*.md'):
        if p.relative_to(root).as_posix() not in expected: p.unlink()
    return len(expected)


def validate(root=ROOT):
    try: rows=read_rows(root)
    except (ValueError,OSError) as e: return [str(e)]
    manifest=json.loads((root/'sources/manifest.json').read_text())
    known={s['id'] for s in manifest['pages']}
    errors=validate_rows(rows,known)
    occurrences=json.loads((root/'sources/vocabulary-occurrences.json').read_text())
    occurrence_map={o['occurrence_id']:o for o in occurrences}
    if len(occurrence_map)!=len(occurrences): errors.append('duplicate occurrence IDs')
    for row in rows:
        for oid in filter(None,row['occurrence_ids'].split(';')):
            if oid not in occurrence_map: errors.append(f'{row["id"]}: unknown occurrence {oid}')
            elif occurrence_map[oid].get('record_id') != row['id']: errors.append(f'{oid}: record mismatch')
            elif occurrence_map[oid]['source_id'] not in row['source_ids'].split(';'): errors.append(f'{oid}: source omitted from row')
    row_map={row['id']:row for row in rows}
    for occurrence in occurrences:
        oid=occurrence['occurrence_id']; rid=occurrence.get('record_id')
        if rid not in row_map or oid not in row_map[rid]['occurrence_ids'].split(';'):
            errors.append(f'{oid}: unlinked occurrence')
        if occurrence['source_id'] not in known:
            errors.append(f'{oid}: unknown source')
    for row in rows:
        if not row['occurrence_ids'].strip(): errors.append(f'{row["id"]}: occurrence links required')
    for s in manifest['pages']:
        for field in ('raw_path','snapshot_path'):
            if not (root/s[field]).is_file(): errors.append(f'missing {s[field]}')
    for attachment in manifest.get('attachments', []):
        if attachment.get('status') != 'archived': continue
        local_path = attachment.get('local_path', '')
        path = root / local_path
        if not local_path or not path.is_file():
            errors.append(f'archived attachment missing: {attachment.get("name")}')
        elif hashlib.sha256(path.read_bytes()).hexdigest() != attachment.get('sha256'):
            errors.append(f'archived attachment hash mismatch: {local_path}')
    for name,body in rendered(root).items():
        p=root/name
        if not p.is_file() or p.read_text(encoding='utf-8')!=body: errors.append(f'stale generated file: {name}')
    linked=set()
    for p in root.rglob('*.md'):
        if any(x.startswith('.') for x in p.relative_to(root).parts): continue
        text=p.read_text(encoding='utf-8')
        # Inline relative links only; source archives retain external Notion/file URIs.
        for target in re.findall(r'\]\(([^\s)]+)\)',text):
            if re.match(r'^[a-zA-Z][\w+.-]*:',target) or target.startswith('#'): continue
            target=unquote(target.split('#')[0])
            if target and not (p.parent/target).exists(): errors.append(f'{p.relative_to(root)}: broken link {target}')
            elif target and (p.parent/target).resolve()!=p.resolve(): linked.add((p.parent/target).resolve())
    # Hand-maintained course and grammar pages must be reachable from another page.
    for p in sorted([*root.glob('course/**/*.md'),*root.glob('wiki/grammar/*.md')]):
        if p.resolve() not in linked: errors.append(f'{p.relative_to(root)}: orphan page (no other page links to it)')
    return errors


TEXT_DIRS = ['wiki/grammar','course','journal','sources/pages']


def search_text(query, root=ROOT, dirs=TEXT_DIRS):
    """Yield (path, line number, line) for Markdown lines containing query."""
    needle=normalized(query)
    for folder in dirs:
        for path in sorted((root/folder).rglob('*.md')):
            for number,line in enumerate(path.read_text(encoding='utf-8').splitlines(),1):
                if needle in normalized(line):
                    yield path.relative_to(root).as_posix(), number, line.strip()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['build','validate','search'])
    parser.add_argument('query',nargs='?',default='')
    parser.add_argument('--all',action='store_true',help='search: also search grammar, course, journal and source pages')
    args=parser.parse_args()
    if args.command=='build': print(f'Generated {build()} reading views')
    elif args.command=='validate':
        errors=validate()
        if errors: print('\n'.join(errors)); return 1
        print(f'Validated {len(read_rows())} vocabulary records; sources, links and generated views are consistent.')
    else:
        needle=normalized(args.query)
        if not needle: parser.error('search requires a query')
        if args.all: print('== Vocabulary ==')
        for row in read_rows():
            if needle in normalized(' '.join(row.values())):
                print(f"{row['id']}\t{row['dutch']}\t{row['english']}\t{VIEWS}/words/{row['id']}.md")
        if args.all:
            current=None
            for path,number,line in search_text(args.query):
                if path!=current:
                    print(f'\n== {path} =='); current=path
                print(f'{number}: {line}')
    return 0

if __name__=='__main__':
    try: sys.exit(main())
    except BrokenPipeError:
        sys.stderr.close(); sys.exit(0)
