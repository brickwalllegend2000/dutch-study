#!/usr/bin/env python3
"""One-time migration from preserved Notion responses. Refuses to replace canonical data."""
import csv
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import parse_qs, urlparse
from library import ROOT, FIELDS, DATA_CSV, parse_tables, plain, consolidate, to_markdown, record_id, build


def body(page):
    return page['text'].split('<content>',1)[1].split('</content>',1)[0].strip()


def slug(title):
    return re.sub(r'[^a-z0-9]+','-',title.casefold()).strip('-')


def main():
    if (ROOT/DATA_CSV).exists(): raise SystemExit(f'Refusing to overwrite {DATA_CSV}. Migration is one-time; use the normal workflow for edits.')
    pages={p.stem:json.loads(p.read_text(encoding='utf-8')) for p in sorted((ROOT/'sources/notion').glob('*.json'))}
    cfg=json.loads((ROOT/'sources/import-config.json').read_text())
    chapters={sid:n for n,sid in enumerate(cfg['chapter_ids'],1)}
    mapping={sid:(f'sources/pages/{sid}.md',p['title']) for sid,p in pages.items()}
    mapping['401f89e5e0fc8054b148fa2fdaf07675']=('README.md','Dutch study')
    for sid in cfg['grammar_ids']: mapping[sid]=(f'grammar/{slug(pages[sid]["title"])}.md',pages[sid]['title'])
    for sid,n in chapters.items(): mapping[sid]=(f'chapters/chapter-{n:02}.md',pages[sid]['title'])
    for sid,p in pages.items():
        if re.search(r'Project [ABC]:|[ABC][123] |Combined projects|Practice Test',p['title']): mapping[sid]=(f'practice/{slug(p["title"])}.md',p['title'])
    inventory=[]; attachments=[]
    for sid,p in pages.items():
        raw=f'sources/notion/{sid}.json'; snapshot=f'sources/pages/{sid}.md'
        item={'id':sid,'title':p['title'],'url':p['url'],'raw_path':raw,'snapshot_path':snapshot,'last_edited_at':p.get('page_last_edited_at'),'retrieval_status':'fetched','linguistic_review':'not-performed'}
        for key in ['truncated','unknown_block_count','unknown_block_ids']:
            if key in p: item[key]=p[key]
        inventory.append(item)
        text=body(p)
        for uri in re.findall(r'<(?:image|file|pdf|audio|video)\b[^>]*(?:source|url)="([^"]+)"',text):
            name=parse_qs(urlparse(uri).query).get('name',['Unnamed original'])[0]
            attachments.append({'source_id':sid,'name':name,'reference':uri,'status':'reference-only','reason':'Notion fetch returned notion-file-block URIs, not downloadable binary URLs.'})
        path=ROOT/snapshot; path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(f'# {p["title"]}\n\n> Preserved import snapshot, 2026-10-23. Not maintained as canonical study data.\n\n[Original Notion page]({p["url"]}) · [Exact retrieval payload](../notion/{sid}.json)\n\n'+to_markdown(text,mapping,snapshot),encoding='utf-8')
        dest=mapping[sid][0]
        if dest.startswith(('grammar/','practice/')):
            path=ROOT/dest;path.parent.mkdir(parents=True,exist_ok=True)
            header='---\nid: '+('GRAM-' if dest.startswith('grammar/') else 'PRACTICE-')+sid[-12:]+'\nsource_ids: ["'+sid+'"]\nreview_status: needs-review\n---\n'
            path.write_text(header+f'# {p["title"]}\n\n> Imported course material; linguistic review pending.\n\n[Source snapshot](../sources/pages/{sid}.md) · [Home](../README.md)\n\n'+to_markdown(text,mapping,dest),encoding='utf-8')
    # Filenames cited by the perfectum transcription, without accessible image blocks.
    for name in ['IMG_1279.jpg','IMG_1280.jpeg','IMG_524C65CB-D2F7-437A-85E8-12C901727869.jpeg','IMG_A1AE6AA3-BC8A-4DB2-936E-13D56B700D6F.jpeg']:
        attachments.append({'source_id':'401f89e5e0fc80f29352c76d2b8204b7','name':name,'reference':'Cited in perfectum source record','status':'reference-only','reason':'Original photo bytes are not attached to the fetched task page.'})
    manifest={'imported_on':'2026-10-23','scope':'Dutch study root, all 8 chapters, all 12 grammar records, directly linked references, combined projects and exercises, and relevant migration tasks. Unrelated task parents and database views were not crawled.','pages':inventory,'attachments':attachments}
    (ROOT/'sources/manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    occurrences=[]
    def add(sid,loc,**fields):
        cleaned={k:plain(str(v)) for k,v in fields.items() if v is not None}
        cleaned={k:('' if v in ('–','—','-') else v) for k,v in cleaned.items()}
        if not cleaned.get('dutch'): return
        occurrence_id='OCC-'+hashlib.sha256((sid+'|'+loc).encode()).hexdigest()[:16]
        occurrences.append({'occurrence_id':occurrence_id,'source_id':sid,'locator':loc,**cleaned})
    master='401f89e5e0fc813ba013ca7c14321902'
    chapter_for_index={}
    for m in re.finditer(r'## Chapter (\d+).*?(?=## |\Z)',body(pages[master]),re.S):
        chapter=m[1]
        for table in parse_tables(m[0]):
            if table[0][:3]!=['#','Article','Word / term']: continue
            for r in table[1:]:
                if len(r)!=8: raise ValueError(f'Unexpected master row {r!r}')
                num,article,dutch,forms,typ,examples,notes,category=r
                chapter_for_index[num]=chapter
                add(master,f'chapter {chapter}, row {num}',dutch=dutch,article=article,forms=forms,word_type=typ,examples=examples,notes=notes,categories=category,chapters=chapter)
    assert len(chapter_for_index)==302, f'Expected 302 master vocabulary occurrences, got {len(chapter_for_index)}'
    for ti,table in enumerate(parse_tables(body(pages[master])),1):
        if table[0]==['Chapter','Dutch','English']:
            for ri,r in enumerate(table[1:],1): add(master,f'table {ti}, row {ri}',chapters=r[0],dutch=r[1],english=r[2])
        elif table[0]==['Verb','Present-tense example and note']:
            for ri,r in enumerate(table[1:],1): add(master,f'table {ti}, row {ri}',dutch=r[0],forms=r[1],word_type='Verbum')
    # Chapter vocabulary contains English meanings missing from the master table.
    for sid,n in chapters.items():
        section=body(pages[sid]).split('## Vocabulary',1)[-1]
        section=re.split(r'\n## (?!Vocabulary)',section,maxsplit=1)[0]
        for ti,table in enumerate(parse_tables(section),1):
            headers=table[0]
            dutch_col=next((i for i,h in enumerate(headers) if h in ('Nederlands','Dutch','Woord','Verbum')),None)
            english_col=next((i for i,h in enumerate(headers) if h in ('English','Engels')),None)
            if dutch_col is None or english_col is None: continue
            for ri,r in enumerate(table[1:],1):
                if len(r)!=len(headers): raise ValueError(f'Chapter {n}: malformed row {r}')
                term=r[dutch_col];article=''
                if term.startswith(('de ','het ')):article,term=term.split(' ',1)
                form_col=next((i for i,h in enumerate(headers) if 'vorm' in h.lower() or 'meervoud' in h.lower()),None)
                add(sid,f'vocabulary table {ti}, row {ri}',dutch=term,article=article,english=r[english_col],forms=r[form_col] if form_col is not None else '',chapters=str(n))
    perfect='401f89e5e0fc80f29352c76d2b8204b7'; perfect_count=0
    for ti,table in enumerate(parse_tables(body(pages[perfect])),1):
        if table[0][:3]!=['No.','Infinitive','English']: continue
        for r in table[1:]:
            if len(r)!=6: raise ValueError('Malformed perfectum table')
            num,dutch,english,aux,part,example=r
            add(perfect,f'perfectum sheet {(int(num)-1)//20+1}, verb {num}',dutch=dutch,english=english,auxiliary=aux,participle=part,examples=example,word_type='Verbum',categories='Perfectum study list',notes='Auxiliary is source-specific; see the source notes for active/passive and movement distinctions.')
            perfect_count+=1
    assert perfect_count==80, f'Expected 80 perfectum verbs, got {perfect_count}'
    irregular='401f89e5e0fc8136967bea7232a7e938'; irregular_count=0
    for ti,table in enumerate(parse_tables(body(pages[irregular])),1):
        if table[0]!=['Infinitief','Perfectum']: continue
        for ri,r in enumerate(table[1:],1):
            m=re.match(r'\(([^)]+)\)\s*(.+)',r[1])
            if not m: raise ValueError('Malformed irregular verb')
            add(irregular,f'irregular table {ti}, row {ri}',dutch=r[0],auxiliary=m[1],participle=m[2],word_type='Verbum',categories='Irregular verbs')
            irregular_count+=1
    rows=consolidate(occurrences)
    csv_path=ROOT/DATA_CSV; csv_path.parent.mkdir(parents=True,exist_ok=True)
    with csv_path.open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=FIELDS);writer.writeheader();writer.writerows(rows)
    for o in occurrences: o['record_id']=record_id(o['dutch'])
    (ROOT/'sources/vocabulary-occurrences.json').write_text(json.dumps(occurrences,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for sid,n in chapters.items():
        p=pages[sid];dest=mapping[sid][0];props=json.loads(p['text'].split('<properties>')[1].split('</properties>')[0])
        topics=[]
        for url in props.get('Grammatica topics',[]):
            match=re.search(r'[a-f0-9]{32}',url)
            if match and match[0] in mapping:
                target,title=mapping[match[0]];topics.append(f'- [{title}](../{target})')
        lines=[f'# Chapter {n}: {p["title"].split(". ",1)[-1]}','',f'[Vocabulary](../views/CHAPTER-{n:02}.md) · [Exercises and preserved chapter text](../sources/pages/{sid}.md) · [Home](../README.md)','','## Grammar','']+topics+['','## Study session','','1. Review vocabulary and choose five terms.','2. Read the linked grammar topic.','3. Complete an exercise from the preserved chapter text.','4. Save your attempt in `study/` using the study-session template.','5. Open a correction issue for uncertain material.','']
        path=ROOT/dest;path.parent.mkdir(parents=True,exist_ok=True);path.write_text('\n'.join(lines),encoding='utf-8')
    summary={'pages':len(pages),'grammar_topics':len(cfg['grammar_ids']),'chapters':len(chapters),'master_vocabulary_occurrences':302,'perfectum_occurrences':perfect_count,'irregular_occurrences':irregular_count,'total_occurrences':len(occurrences),'canonical_vocabulary_records':len(rows),'attachment_references':len(attachments),'unique_referenced_original_names':len({a['name'] for a in attachments}),'original_binary_files_downloaded':0}
    (ROOT/'sources/import-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2));print(f'Generated {build()} views')

if __name__=='__main__': main()
