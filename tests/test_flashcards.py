import json
import re
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


class FlashcardTests(unittest.TestCase):
    def test_every_deck_is_present(self):
        d = data()
        self.assertEqual({c['k'] for c in d['cards']}, {'vocab', 'perfectum', 'imperfectum', 'grammar'})
        for deck in ('cloze', 'dehet', 'aux', 'adj', 'quiz', 'writing'):
            self.assertTrue(d[deck], deck)
        self.assertEqual(len(d['writing']), 6)

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

    def test_markdown_is_escaped(self):
        self.assertEqual(flashcards.md_to_html('- <b>x</b> **y**'), '<ul><li>&lt;b&gt;x&lt;/b&gt; <b>y</b></li></ul>')

    def test_generated_page_is_current(self):
        page = (ROOT / 'views/vocabulary/flashcards.html').read_text(encoding='utf-8')
        self.assertEqual(page, flashcards.render(library.read_rows(), ROOT))


if __name__ == '__main__':
    unittest.main()
