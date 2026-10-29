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
        raw = r['auxiliary'].lower()
        auxs = [a for a, w in (('heeft', 'hebben heeft'), ('is', 'zijn is')) if any(x in raw.split() or x in raw.replace('/', ' ').replace(';', ' ').split() for x in w.split())]
        parts = [p.strip() for p in re.split(r'[;/,]', r['participle']) if p.strip()]
        perfectum.append({**base, 'k': 'perfectum', 'tags': [], 'f': r['dutch'],
                          'ans': parts + [a + ' ' + p for a in auxs for p in parts],
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
                      'ex': r['examples'].replace('\u00ab', '').replace('\u00bb', '').strip(),
                      'forms': r['forms']})
    return cards


def cloze_cards(rows):
    """Blank the whole word that contains the headword in the example sentence."""
    cards = []
    for r in rows:
        ex = r['examples'].replace('\u00ab', '').replace('\u00bb', '').strip()
        head = re.sub(r'\(.*?\)', '', r['dutch']).strip().lower()
        if not ex or not head or r['word_type'].lower().startswith(('zin', 'functionele')):
            continue
        m = re.search(r'\b(\w*' + re.escape(head.split(' ')[-1]) + r'\w*)\b', ex, re.I) if ' ' in head else \
            re.search(r'\b(\w*' + re.escape(head) + r'\w*)\b', ex, re.I)
        if not m or len(m.group(1)) < 3:
            continue
        cards.append({'id': r['id'], 'r': r['review_status'], 'tags': [word_group(r)],
                      'f': ex[:m.start()] + '_____' + ex[m.end():], 'ans': m.group(1),
                      'hint': r['dutch'], 'en': r['english'], 'full': ex})
    return cards


def drill_cards(rows):
    reviewed = [r for r in rows if r['review_status'] == 'reviewed']
    seen, dehet = set(), []
    for r in reviewed:
        w = r['dutch']
        if r['article'] in ('de', 'het') and w not in seen and ' ' not in w and '(' not in w:
            seen.add(w)
            dehet.append({'id': r['id'], 'w': w, 'art': r['article'], 'en': r['english']})
    aux = []
    for r in reviewed:
        a = {'hebben': 'heeft', 'heeft': 'heeft', 'zijn': 'is', 'is': 'is'}.get(r['auxiliary'])
        if r['participle'] and a:
            aux.append({'id': r['id'], 'w': r['dutch'], 'aux': a, 'part': r['participle'], 'en': r['english']})
    return dehet, aux


# Hand-checked inflections (adjective before a de-word, plural or definite noun).
ADJ_E = {'blauw': 'blauwe', 'bruin': 'bruine', 'diep': 'diepe', 'dik': 'dikke', 'geel': 'gele',
         'grijs': 'grijze', 'groen': 'groene', 'paars': 'paarse', 'rond': 'ronde', 'rood': 'rode',
         'wit': 'witte', 'zwart': 'zwarte', 'zwaar': 'zware', 'ruim': 'ruime', 'mooi': 'mooie',
         'modern': 'moderne', 'vierkant': 'vierkante', 'rechthoekig': 'rechthoekige',
         'gezellig': 'gezellige', 'prachtig': 'prachtige', 'rustig': 'rustige', 'ovaal': 'ovale',
         'vuil': 'vuile', 'lichtblauw': 'lichtblauwe', 'donkergroen': 'donkergroene',
         'gestreept': 'gestreepte', 'geruit': 'geruite', 'gebloemd': 'gebloemde'}
NEVER_E = ('effen', 'glazen', 'houten', 'ijzeren', 'katoenen', 'leren', 'stenen', 'stoffen', 'wollen',
           'roze', 'oranje', 'beige', 'plastic')


def adjective_cards(rows):
    import random
    rnd = random.Random(7)
    nouns = [r for r in rows if r['review_status'] == 'reviewed' and r['article'] in ('de', 'het')
             and ' ' not in r['dutch'] and '(' not in r['dutch'] and r['dutch'][0].islower()]
    present = {p.strip() for r in rows if 'adject' in r['word_type'].lower() for p in re.split(r'\s*[\u2194/]\s*', r['dutch'])}
    cards = []
    for adj in list(ADJ_E) + list(NEVER_E):
        if adj not in present:
            continue
        never = adj in NEVER_E
        for n in rnd.sample(nouns, 3):
            art, noun = n['article'], n['dutch']
            infl = adj if never else ADJ_E[adj]
            # (frame, takes -e?, article shown in the full sentence)
            frames = [(f'Een ___ {noun}', art == 'de' or never, f'Een {{a}} {noun}'),
                      (f'{art.capitalize()} ___ {noun}', True, f'{art.capitalize()} {{a}} {noun}'),
                      (f'{art.capitalize()} {noun} is ___.', False, f'{art.capitalize()} {noun} is {adj}.')]
            for fr, with_e, full in frames:
                if never:
                    with_e = False
                cards.append({'id': f'{adj}-{noun}-{len(cards)}', 'adj': adj, 'f': fr, 'e': with_e,
                              'full': full.format(a=infl if with_e else adj), 'never': never})
    rnd.shuffle(cards)
    return cards[:180]


def quiz_items(root):
    path = Path(root) / 'data/grammar-quiz.json'
    if not path.exists():
        return []
    items = json.loads(path.read_text(encoding='utf-8'))['items']
    titles = {}
    for p in (Path(root) / 'data/grammar').glob('*.md'):
        m = re.search(r'^# (.+)$', p.read_text(encoding='utf-8'), re.M)
        if m:
            titles[p.relative_to(root).as_posix()] = m.group(1).strip()
    for it in items:
        it['topic'] = titles.get(it['note'], 'Imperfectum (past tense)' if it['note'] == 'imperfectum' else it['note'])
    return items


def writing_prompts(root):
    path = Path(root) / 'course/exercises/schrijfopdrachten.md'
    if not path.exists():
        return []
    prompts = []
    for block in re.split(r'^## Oefening ', path.read_text(encoding='utf-8'), flags=re.M)[1:]:
        head, _, body = block.partition('\n')
        num, _, title = head.partition(' \u2014 ')
        body = body.split('> Geef hier')[0].replace('\n---', '')
        instr = [re.sub(r'\*+', '', l).strip() for l in body.splitlines() if l.startswith('**')]
        m = re.search(r'(minimum|in) (\d+) zinnen', ' '.join(instr))
        rest = [l for l in body.splitlines() if l.strip() and not l.startswith('**')]
        text = '\n'.join(re.sub(r'^> ?', '', l).replace('\\', '') for l in rest)
        text = re.sub(r'\*\*|^\*|\*$', '', text, flags=re.M)
        low = (title + body).lower()
        theme = ('Meubels & Inrichting' if 'woonkamer' in low else 'Kleuren' if 'foto' in low
                 else 'Stad, Toerisme & Reizen' if 'trein' in low else '')
        prompts.append({'id': 'W' + num.strip(), 'title': title.strip(), 'instr': instr, 'min': int(m.group(2)) if m else 0,
                        'exact': bool(m and m.group(1) == 'in'), 'text': text,
                        'questions': [l.strip() for l in text.splitlines() if l.strip().endswith('?')],
                        'photo': 'foto' in low, 'theme': theme})
    return prompts


def render(rows, root):
    dehet, aux = drill_cards(rows)
    data = {'cards': vocab_cards(rows) + verb_cards(rows) + grammar_cards(Path(root)),
            'cloze': cloze_cards(rows), 'dehet': dehet, 'aux': aux,
            'adj': adjective_cards(rows), 'quiz': quiz_items(root),
            'writing': writing_prompts(root)}
    blob = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
    template = (Path(__file__).resolve().parent / 'flashcards_template.html').read_text(encoding='utf-8')
    return template.replace('__DATA__', blob)
