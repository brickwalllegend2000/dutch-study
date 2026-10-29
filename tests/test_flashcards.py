import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import flashcards
import library


def cards():
    page = flashcards.render(library.read_rows(), ROOT)
    return json.loads(re.search(r'const ALL=(.*);\nconst \$', page).group(1))


class FlashcardTests(unittest.TestCase):
    def test_every_kind_is_present(self):
        kinds = {c['k'] for c in cards()}
        self.assertEqual(kinds, {'vocab', 'perfectum', 'imperfectum', 'grammar'})

    def test_vocab_cards_cover_every_row(self):
        self.assertEqual(sum(c['k'] == 'vocab' for c in cards()), len(library.read_rows()))

    def test_imperfectum_only_from_simple_pairs(self):
        for c in cards():
            if c['k'] == 'imperfectum':
                self.assertNotIn('ik', c['sub'].split())

    def test_markdown_is_escaped(self):
        self.assertEqual(flashcards.md_to_html('- <b>x</b> **y**'), '<ul><li>&lt;b&gt;x&lt;/b&gt; <b>y</b></li></ul>')

    def test_generated_page_is_current(self):
        page = (ROOT / 'views/vocabulary/flashcards.html').read_text(encoding='utf-8')
        self.assertEqual(page, flashcards.render(library.read_rows(), ROOT))


if __name__ == '__main__':
    unittest.main()
