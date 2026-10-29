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


    def test_mastery_counts_cards_per_box_and_practice_days(self):
        out = node(js('boxCounts', 'dayStrip') + """
const P={a:{b:0},b:{b:6},c:{b:2},d:{b:2}};
console.log(JSON.stringify([boxCounts(['a','b','c','d','e','f'],P),dayStrip({100:3,95:1,80:9},100).filter(([,n])=>n),dayStrip({},100).length]))""")
        self.assertEqual(out, [[2, 1, 0, 2, 0, 0, 0, 1], [[95, 1], [100, 3]], 14])


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

    def test_grammar_markup_marks_patterns_and_examples(self):
        html = flashcards.md_to_html('**Subject + verb.**\n\n- **Ik ga.** — I go.\n- plain item\n\n**Used in**')
        self.assertEqual(html, '<p class="pat"><b>Subject + verb.</b></p><ul><li class="ex"><b>Ik ga.</b> — I go.</li>'
                               '<li>plain item</li></ul><p><b>Used in</b></p>')

    def test_cheatsheet_tables_parse(self):
        c = flashcards.cheatsheet(ROOT)
        self.assertEqual(len(c['types']), 7)
        self.assertTrue(all(t['steps'] for t in c['types'].values()))
        self.assertEqual(len(c['spelling']), 5)
        self.assertEqual(len(c['final']), 5)
        self.assertGreaterEqual(len(c['bank']), 11)
        self.assertEqual(c['types']['Formulier']['phrases'], [])
        self.assertIn('met vriendelijke groeten,', c['types']['Briefje, formeel']['phrases'])

    def test_every_task_type_exists_and_four_tasks_have_none(self):
        types = flashcards.cheatsheet(ROOT)['types']
        for tid, name in flashcards.TASK_TYPES.items():
            self.assertIn(name, types, tid)
        prompts = data()['writing']
        self.assertEqual({p['id'] for p in prompts if not p['type']}, {'W1', 'W3', 'W4', 'W5'})
        self.assertEqual(len([p for p in prompts if p['type']]), 11)

    def test_checklists_add_type_items_after_the_generic_ones(self):
        by_id = {p['id']: p for p in data()['writing']}
        self.assertEqual(by_id['W1']['extra'], [])
        form = by_id['E1']['extra']
        self.assertTrue(form[0].startswith('Followed the structure'))
        self.assertTrue(any('Postcode' in x for x in form))
        self.assertFalse(any('minimum number' in x for x in form))
        self.assertTrue(any('minimum number' in x for x in by_id['W2']['extra']))
        self.assertFalse(any('Postcode' in x for x in by_id['W2']['extra']))

    def test_phrase_deck_accepts_slash_alternatives_without_slashes(self):
        cards = data()['phrases']
        self.assertEqual(len(cards), len(flashcards.cheatsheet(ROOT)['bank']))
        self.assertEqual(len({c['id'] for c in cards}), len(cards))
        by_nl = {c['nl']: c for c in cards}
        self.assertEqual(len(by_nl['Tot snel / straks / morgen / vanavond.']['ans']), 4)
        self.assertIn('Bedankt voor uw e-mail.', by_nl['Bedankt voor je/uw e-mail.']['ans'])
        for c in cards:
            self.assertFalse(any('/' in a for a in c['ans']), c['id'])
            self.assertEqual(c['origin'], 'imported')

    def test_trial_explanations_cover_each_model_sentence_and_stay_apart(self):
        by_id = {p['id']: p for p in data()['writing']}
        self.assertEqual({k for k, p in by_id.items() if p['model']['notes']}, {'E2', 'E9'})
        for tid in ('E2', 'E9'):
            m = by_id[tid]['model']
            self.assertNotIn('---', m['en'])
            self.assertNotIn('Uitleg', m['nl'] + m['en'])
            for n in m['notes']:
                self.assertTrue(n['label'] and n['nl'] and n['note'], n)
                self.assertNotIn('*', n['nl'] + n['note'])
                self.assertIn(n['nl'].split(' ')[0].rstrip(',.!?'), m['nl'], n)

    def test_generated_page_is_current(self):
        page = (ROOT / 'views/vocabulary/flashcards.html').read_text(encoding='utf-8')
        self.assertEqual(page, flashcards.render(library.read_rows(), ROOT))


if __name__ == '__main__':
    unittest.main()
