"""Generate the self-contained flashcard page from the CSV and grammar notes."""
import html
import json
import re
from pathlib import Path

SKIP_HEADINGS = ('sources', 'review note', 'try it', 'use it with', 'examples from the archive')
META_THEMES = {'Perfectum study list', 'Irregular verbs', 'Verbs'}


def word_group(row):
    t = row['word_type'].lower()
    if row['participle'] or t.startswith(('verb', 'verba')):
        return 'Verbs'
    if 'adject' in t:
        return 'Adjectives'
    if 'prepositie' in t:
        return 'Prepositions'
    if 'zin' in t or 'verbinding' in t:
        return 'Phrases'
    if t.startswith(('subst', 'noun')) or row['article']:
        return 'Nouns'
    return 'Other'


def _inline(text):
    text = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', text)
    text = html.escape(text, quote=False)
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    return re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<i>\1</i>', text)


def md_to_html(md):
    out, lines, i = [], md.strip().splitlines(), 0
    while i < len(lines):
        line = lines[i].rstrip()
        if line.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                cells = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?', c) for c in cells):
                    rows.append(cells)
                i += 1
            out.append('<table>' + ''.join(
                '<tr>' + ''.join(('<th>' if n == 0 else '<td>') + _inline(c) for c in r) + '</tr>'
                for n, r in enumerate(rows)) + '</table>')
            continue
        if re.match(r'\s*[-*] ', line):
            items = []
            while i < len(lines) and re.match(r'\s*[-*] ', lines[i]):
                items.append('<li>' + _inline(re.sub(r'^\s*[-*] ', '', lines[i])) + '</li>')
                i += 1
            out.append('<ul>' + ''.join(items) + '</ul>')
            continue
        if line.strip() and not line.startswith('>'):
            out.append('<p>' + _inline(line) + '</p>')
        i += 1
    return ''.join(out)


def grammar_cards(root):
    cards = []
    for path in sorted((root / 'data/grammar').glob('*.md')):
        if path.name == 'README.md':
            continue
        text = path.read_text(encoding='utf-8')
        title = re.search(r'^# (.+)$', text, re.M)
        review = re.search(r'^review_status: (\S+)', text, re.M)
        if not title:
            continue
        title = title.group(1).strip()
        body = text[text.index(title) + len(title):]
        parts = re.split(r'^(#{2,3}) (.+)$', body, flags=re.M)
        parent = ''
        for n in range(1, len(parts) - 2, 3):
            level, head, content = parts[n], parts[n + 1].strip(), parts[n + 2]
            if level == '##':
                parent = head
            if head.lower().startswith(SKIP_HEADINGS) or parent.lower().startswith(SKIP_HEADINGS):
                continue
            if level == '##' and '### ' in content:
                content = content.split('### ')[0]
            content = md_to_html(content)
            if len(content) < 30:
                continue
            cards.append({'k': 'grammar', 'tags': [title], 'f': title, 'sub': head,
                          'b': content, 'src': path.relative_to(root).as_posix(),
                          'r': review.group(1) if review else ''})
    return cards


def verb_cards(rows):
    perfectum, imperfectum = [], []
    for r in rows:
        if not r['participle']:
            continue
        aux = {'hebben': 'heeft', 'heeft': 'heeft', 'zijn': 'is', 'is': 'is'}.get(r['auxiliary'], r['auxiliary'])
        base = {'r': r['review_status'], 'id': r['id'], 'en': r['english']}
        perfectum.append({**base, 'k': 'perfectum', 'tags': [], 'f': r['dutch'],
                          'b': f"<b>{html.escape(aux)} {html.escape(r['participle'])}</b>"})
        forms = r['forms']
        # Only simple "present, past" pairs are safe to read as imperfectum.
        if forms and not re.search(r'[⟐;/]|\bik\b|\(', forms):
            pair = [p.strip() for p in forms.split(',')]
            if len(pair) == 2 and pair[0] != pair[1]:
                imperfectum.append({**base, 'k': 'imperfectum', 'tags': [], 'f': r['dutch'],
                                    'b': f"<b>{html.escape(pair[1])}</b>",
                                    'sub': f"present: {html.escape(pair[0])}"})
    return perfectum + imperfectum


def vocab_cards(rows):
    themes = {}
    for r in rows:
        for c in r['categories'].split(';'):
            c = c.strip()
            if c and c not in META_THEMES:
                themes[c] = themes.get(c, 0) + 1
    cards = []
    for r in rows:
        tags = [word_group(r)] + [c.strip() for c in r['categories'].split(';')
                                   if themes.get(c.strip(), 0) >= 3]
        tags += ['Chapter ' + c for c in r['chapters'].split(';') if c]
        cards.append({'k': 'vocab', 'tags': tags, 'id': r['id'], 'r': r['review_status'],
                      'art': r['article'], 'nl': r['dutch'], 'en': r['english'],
                      'ex': r['examples'].replace('«', '').replace('»', '').strip(),
                      'forms': r['forms']})
    return cards


def render(rows, root):
    cards = vocab_cards(rows) + verb_cards(rows) + grammar_cards(Path(root))
    data = json.dumps(cards, ensure_ascii=False).replace('</', '<\\/')
    return TEMPLATE.replace('__DATA__', data)


TEMPLATE = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Dutch flashcards</title>
<!-- Generated by scripts/flashcards.py via `python scripts/library.py build`. Do not edit. -->
<style>
:root{--bg:#fafaf7;--fg:#1d1d1b;--mut:#6b6b66;--card:#fff;--bd:#d9d9d2;--ac:#e8590c;--ok:#2b8a3e;--no:#c92a2a}
@media(prefers-color-scheme:dark){:root{--bg:#161615;--fg:#eee;--mut:#9a9a94;--card:#212120;--bd:#383835}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.5 system-ui,sans-serif}
main{max-width:640px;margin:0 auto;padding:16px}
h1{font-size:20px;margin:0 0 12px}
.ctl{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:12px}
.ctl label{font-size:12px;color:var(--mut);display:flex;flex-direction:column;gap:2px}
select,button,input{font:inherit;padding:8px;border-radius:8px;border:1px solid var(--bd);background:var(--card);color:var(--fg)}
.full{grid-column:1/-1}.chk{flex-direction:row!important;align-items:center;gap:6px!important;font-size:13px!important}
.card{min-height:230px;background:var(--card);border:1px solid var(--bd);border-radius:14px;padding:20px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;cursor:pointer}
.big{font-size:30px;font-weight:650}.sub{color:var(--mut);margin-top:10px}.tiny{font-size:12px;color:var(--mut);margin-top:12px}
.back{width:100%;text-align:left}.back table{border-collapse:collapse;margin:8px 0;font-size:14px}.back td,.back th{border:1px solid var(--bd);padding:4px 8px}
.back ul{padding-left:20px;margin:6px 0}.back p{margin:6px 0}
.bar{display:flex;gap:8px;margin-top:12px;align-items:center}.bar .st{flex:1;color:var(--mut);font-size:13px}
.no{background:var(--no);color:#fff;border:0}.ok{background:var(--ok);color:#fff;border:0}.pri{background:var(--ac);color:#fff;border:0}
.flag{color:#b8860b}
</style></head><body><main>
<h1>Dutch flashcards</h1>
<div class="ctl">
 <label>Practise<select id="kind">
  <option value="vocab">Vocabulary</option>
  <option value="perfectum">Perfectum (verb → heeft/is + participle)</option>
  <option value="imperfectum">Imperfectum (verb → past form)</option>
  <option value="grammar">Grammar rules</option></select></label>
 <label>Filter<select id="filter"></select></label>
 <label id="dirL">Direction<select id="dir"><option value="nl">Dutch → English</option><option value="en">English → Dutch</option></select></label>
 <label>Order<select id="ord"><option value="r">Shuffled</option><option value="o">In order</option></select></label>
 <label class="chk full"><input type="checkbox" id="nr"> Include cards not yet linguistically reviewed</label>
</div>
<div class="card" id="card" tabindex="0"></div>
<div class="bar"><span class="st" id="st"></span>
 <button id="flip">Flip</button><button class="no" id="again">Again</button><button class="ok" id="got">Got it</button></div>
<p class="tiny">Space = flip · ← again · → got it. Progress is not saved; reload to restart. Facts come from data/vocabulary.csv and data/grammar/.</p>
</main>
<script>
const ALL=__DATA__;
const $=id=>document.getElementById(id);
const esc=s=>String(s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
let deck=[],known=0,shown=false;
function opts(){
 const k=$('kind').value,f=$('filter');f.innerHTML='';
 const add=(v,t)=>f.add(new Option(t,v));
 add('','All');
 if(k==='vocab'){
  const tags={};ALL.filter(c=>c.k==='vocab').forEach(c=>c.tags.forEach(t=>tags[t]=(tags[t]||0)+1));
  const types=['Nouns','Verbs','Adjectives','Prepositions','Phrases','Other'];
  const g1=document.createElement('optgroup');g1.label='By word type';
  types.filter(t=>tags[t]).forEach(t=>g1.appendChild(new Option(t+' ('+tags[t]+')',t)));f.appendChild(g1);
  const g2=document.createElement('optgroup');g2.label='By chapter';
  Object.keys(tags).filter(t=>t.startsWith('Chapter ')).sort().forEach(t=>g2.appendChild(new Option(t+' ('+tags[t]+')',t)));f.appendChild(g2);
  const g3=document.createElement('optgroup');g3.label='By theme';
  Object.keys(tags).filter(t=>!types.includes(t)&&!t.startsWith('Chapter ')).sort().forEach(t=>g3.appendChild(new Option(t+' ('+tags[t]+')',t)));f.appendChild(g3);
 }else if(k==='grammar'){
  [...new Set(ALL.filter(c=>c.k==='grammar').map(c=>c.f))].sort().forEach(t=>add(t,t));
 }
 $('dirL').style.display=k==='vocab'?'':'none';
 f.style.display=(k==='perfectum'||k==='imperfectum')?'none':'';
 start();
}
function start(){
 const k=$('kind').value,flt=$('filter').value,nr=$('nr').checked;
 deck=ALL.filter(c=>c.k===k&&(nr||c.r!=='needs-review')&&(!flt||c.tags.includes(flt)));
 if($('ord').value==='r')for(let i=deck.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[deck[i],deck[j]]=[deck[j],deck[i]];}
 known=0;shown=false;draw();
}
function faces(c){
 const k=c.k,flag=c.r==='needs-review'?'<div class="tiny flag">not yet reviewed</div>':'';
 if(k==='vocab'){
  const nl=(c.art?c.art+' ':'')+c.nl,rev=$('dir').value==='en';
  const front=rev?c.en:nl,back=rev?nl:c.en;
  return [`<div class="big">${esc(front)}</div>`,
   `<div class="big">${esc(back)}</div>`+(rev?'':'')+(c.ex?`<div class="sub">${esc(c.ex)}</div>`:'')+(c.forms?`<div class="sub">${esc(c.forms)}</div>`:'')+`<div class="tiny">${c.id}</div>`+flag];
 }
 if(k==='perfectum'||k==='imperfectum')
  return [`<div class="big">${esc(c.f)}</div><div class="sub">${esc(c.en)}</div><div class="tiny">${k==='perfectum'?'perfectum: heeft/is + participle':'imperfectum (singular)'}</div>`,
   `<div class="big">${c.b}</div>${c.sub?`<div class="sub">${c.sub}</div>`:''}<div class="sub">${esc(c.f)} — ${esc(c.en)}</div><div class="tiny">${c.id}</div>`+flag];
 return [`<div class="big">${esc(c.sub)}</div><div class="sub">${esc(c.f)}</div>`,
  `<div class="back">${c.b}</div><div class="tiny">${c.src}</div>`+flag];
}
function draw(){
 const card=$('card');
 if(!deck.length){card.innerHTML=known?`<div class="big">Done 🎉</div><div class="sub">${known} cards known</div>`:'<div class="sub">No cards for this selection.</div>';$('st').textContent='';return}
 const f=faces(deck[0]);card.innerHTML=shown?f[1]:f[0]+'<div class="tiny">tap to flip</div>';
 $('st').textContent=deck.length+' left · '+known+' known';
}
const flip=()=>{if(deck.length){shown=!shown;draw()}};
function next(ok){if(!deck.length)return;const c=deck.shift();if(ok)known++;else deck.push(c);shown=false;draw()}
$('card').onclick=$('flip').onclick=flip;$('got').onclick=()=>next(1);$('again').onclick=()=>next(0);
['filter','dir','ord','nr'].forEach(i=>$(i).onchange=start);$('kind').onchange=opts;
document.onkeydown=e=>{if(e.target.tagName==='SELECT')return;if(e.key===' '){e.preventDefault();flip()}else if(e.key==='ArrowRight')next(1);else if(e.key==='ArrowLeft')next(0)};
opts();
</script></body></html>
'''
