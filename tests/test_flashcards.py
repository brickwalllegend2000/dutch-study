import json
import re
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import flashcards
import library


def data():
    page = flashcards.render(library.read_rows(), ROOT)
    return json.loads(re.search(r'const D=(.*);\nconst \$', page).group(1))


def js(*names):
    """Source of top-level declarations from the page script, for running under node."""
    src = (ROOT / 'scripts/flashcards_template.html').read_text(encoding='utf-8')
    out = []
    for name in names:
        start = re.search(r'^(?:function |const )' + re.escape(name) + r'\b', src, re.M).start()
        depth, i = 0, src.index('{', start)
        while True:
            depth += {'{': 1, '}': -1}.get(src[i], 0)
            i += 1
            if depth == 0:
                break
        out.append(src[start:src.index('\n', i)])
    return '\n'.join(out)


def node(code):
    return json.loads(subprocess.run(['node', '-e', code], capture_output=True, text=True, check=True).stdout)


@unittest.skipUnless(shutil.which('node'), 'node not installed')
class PageLogicTests(unittest.TestCase):
    def test_session_state_machine(self):
        out = node(js('IDLE', 'reduce') + """
const a={key:'a',input:'typed'},b={key:'b',input:'flip'};
let s=reduce(IDLE,{type:'start',queue:[a,b]});const log=[s.status];
s=reduce(s,{type:'reveal'});log.push(s.status);
s=reduce(s,{type:'answer',ok:false,input:'x'});log.push(s.status+':'+s.result);
s=reduce(s,{type:'answer',ok:true});log.push(s.result);
s=reduce(s,{type:'next'});log.push(s.cur.key,s.queue.map(c=>c.key).join());
s=reduce(s,{type:'reveal'});log.push(s.status);
s=reduce(s,{type:'answer',ok:true});s=reduce(s,{type:'next'});log.push(s.cur.key);
s=reduce(s,{type:'answer',ok:false});s=reduce(s,{type:'override'});log.push(s.result,s.missed.length);
s=reduce(s,{type:'next'});log.push(s.status,s.done,s.total);
console.log(JSON.stringify(log))""")
        self.assertEqual(out, ['asking', 'asking', 'answered:wrong', 'wrong', 'b', 'a', 'revealed', 'a',
                               'right', 0, 'idle', 2, 2])


    def test_letter_diff_marks_the_differing_letters(self):
        cases = [['gegeeten', 'gegeten'], ['gegetn', 'gegeten'], ['gegaten', 'gegeten'],
                 ['Gegeten', 'gegeten'], ['', 'is'], ['heeft gegeten', 'gegeten']]
        out = node(js('letterDiff') + f"""
const marks=p=>p.map(([c,ok])=>ok?c:'['+c+']').join('');
console.log(JSON.stringify({json.dumps(cases)}.map(([a,b])=>{{const d=letterDiff(a,b);return [marks(d.typed),marks(d.answer)]}})))""")
        self.assertEqual(out, [['gege[e]ten', 'gegeten'], ['gegetn', 'geget[e]n'], ['geg[a]ten', 'geg[e]ten'],
                               ['Gegeten', 'gegeten'], ['', '[i][s]'], ['[h][e][e][f][t][ ]gegeten', 'gegeten']])


class FlashcardTests(unittest.TestCase):
    def test_every_deck_is_present(self):
        d = data()
        self.assertEqual({c['k'] for c in d['cards']}, {'vocab', 'perfectum', 'imperfectum', 'grammar'})
        for deck in ('cloze', 'dehet', 'aux', 'adj', 'quiz', 'writing'):
            self.assertTrue(d[deck], deck)
        self.assertEqual(len(d['writing']), 15)
        for w in d['writing']:
            self.assertTrue(w['model']['nl'] and w['model']['en'], w['id'])

    def test_vocab_cards_cover_every_row(self):
        d = data()
        self.assertEqual(sum(c['k'] == 'vocab' for c in d['cards']), len(library.read_rows()))

    def test_imperfectum_only_from_simple_pairs(self):
        for c in data()['cards']:
            if c['k'] == 'imperfectum':
                self.assertNotIn('ik', c['sub'].split())

    def test_perfectum_answers_accept_bare_participle(self):
        for c in data()['cards']:
            if c['k'] == 'perfectum':
                self.assertTrue(c['ans'], c['f'])

    def test_cloze_blanks_the_answer(self):
        for c in data()['cloze']:
            self.assertIn('_____', c['f'])
            self.assertIn(c['ans'].lower(), c['full'].lower())

    def test_adjective_drill_follows_the_rule(self):
        for c in data()['adj']:
            if c['never'] or c['f'].endswith('___.'):
                self.assertFalse(c['e'], c['f'])
            if c['f'].startswith(('De ___', 'Het ___')):
                self.assertTrue(c['e'] or c['never'])

    def test_quiz_items_are_well_formed(self):
        for q in data()['quiz']:
            self.assertTrue(0 <= q['answer'] < len(q['choices']), q['id'])
            self.assertIn(q['origin'], {'course', 'constructed', 'external', 'course-forms'})
            if q['note'] != 'imperfectum':
                self.assertTrue((ROOT / q['note']).exists(), q['id'])

    def test_concept_rules_are_quoted_from_their_note(self):
        d = data()
        drills = [c for c in d['cards'] if c['k'] == 'perfectum'] + d['aux'] + d['adj'] + d['quiz']
        notes = {}
        for item in drills:
            c = item['concept']
            if c['path'] is None:
                self.assertEqual(item.get('note'), 'imperfectum')
                continue
            if c['path'] not in notes:
                text = (ROOT / c['path']).read_text(encoding='utf-8')
                notes[c['path']] = ' '.join(flashcards.plain(l) for l in text.splitlines())
            self.assertIn(c['rule'], notes[c['path']] if 'why' not in item else item['why'])
            self.assertTrue(c['topic'])
        quiz_paths = {q['concept']['path'] for q in d['quiz']}
        self.assertTrue(all(p is None or (ROOT / p).exists() for p in quiz_paths))

    def test_adjective_concept_matches_the_frame(self):
        for c in data()['adj']:
            rule = c['concept']['rule']
            if c['never']:
                expected = 'c. eindigend op -e' if c['adj'].endswith('e') else ('a. eindigend op -en', 'b. materiaal')
            elif c['f'].endswith('___.'):
                expected = 'a. Na het substantief'
            elif c['f'].startswith('Een'):
                expected = 'de-woord' if c['e'] else 'het-woord'
            else:
                expected = 'de-woord' if c['f'].startswith('De') else 'het-woord'
            self.assertTrue(rule.startswith(expected), (c['f'], rule))

    def test_article_drill_admits_there_is_no_rule(self):
        for c in data()['dehet']:
            self.assertEqual(c['concept'], {'topic': 'de or het', 'rule': None, 'path': None})

    def test_markdown_is_escaped(self):
        self.assertEqual(flashcards.md_to_html('- <b>x</b> **y**'), '<ul><li>&lt;b&gt;x&lt;/b&gt; <b>y</b></li></ul>')

    def test_generated_page_is_current(self):
        page = (ROOT / 'views/vocabulary/flashcards.html').read_text(encoding='utf-8')
        self.assertEqual(page, flashcards.render(library.read_rows(), ROOT))


if __name__ == '__main__':
    unittest.main()
