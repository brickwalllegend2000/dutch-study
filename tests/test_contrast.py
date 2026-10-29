"""Text contrast of the practice page palette, computed from the CSS custom properties."""
import re
import unittest
from pathlib import Path

CSS = (Path(__file__).resolve().parents[1] / 'scripts/flashcards_template.html').read_text(encoding='utf-8')
BACKGROUNDS = ('bg', 'card', 'card2', 'okbg', 'nobg')
TEXT_ON_SURFACES = ('fg', 'mut', 'ok', 'no', 'ac', 'flag', 'de', 'het', 'heeft', 'is')
FILLED = (('onfill', 'ac'), ('onfill', 'ok'), ('onfill', 'no'))


def palette(selector):
    block = re.search(re.escape(selector) + r'\{([^}]*)\}', CSS).group(1)
    return dict(re.findall(r'--([\w-]+):(#[0-9a-fA-F]{6})', block))


def luminance(hex_colour):
    channels = [int(hex_colour[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    r, g, b = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def themes():
    light = palette(':root')
    dark = {**light, **palette(':root[data-theme=dark]')}
    return {'light': light, 'dark': dark}


def failures(colours):
    pairs = [(t, b) for t in TEXT_ON_SURFACES for b in BACKGROUNDS] + list(FILLED)
    return [(t, b, round(ratio(colours[t], colours[b]), 2)) for t, b in pairs if ratio(colours[t], colours[b]) < 4.5]


class ContrastTests(unittest.TestCase):
    def test_all_text_meets_4_5_to_1_in_both_themes(self):
        for name, colours in themes().items():
            self.assertEqual(failures(colours), [], name)

    def test_system_dark_matches_manual_dark(self):
        system = re.search(r':root:not\(\[data-theme=light\]\)\{([^}]*)\}', CSS).group(1)
        self.assertEqual(dict(re.findall(r'--([\w-]+):(#[0-9a-fA-F]{6})', system)), palette(':root[data-theme=dark]'))


if __name__ == '__main__':
    for name, colours in themes().items():
        worst = min(ratio(colours[t], colours[b]) for t in TEXT_ON_SURFACES for b in BACKGROUNDS)
        print(name, 'lowest', round(worst, 2), 'failures', failures(colours))
