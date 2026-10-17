#!/usr/bin/env python3
"""End-to-end tests of the built fonts: python3 -m unittest discover -s test

They shape text with HarfBuzz against build/iosevka-dynamo-*.ttf, so they
need the uharfbuzz module and a previous run of scripts/build.sh; they are
skipped until then.
"""

import sys
import unittest
from os import path

sys.path.insert(0, path.join(path.dirname(__file__), "..", "src"))

from factory.firacode import CHAR_DICT, LIGATURES  # noqa: E402

try:
    import uharfbuzz as hb
except ImportError:  # pragma: no cover
    hb = None

BUILD_DIR = path.join(path.dirname(__file__), "..", "build")
BUILT_FONTS = [
    path.join(BUILD_DIR, "iosevka-dynamo-%s.ttf" % style)
    for style in ("regular", "italic", "bold", "bolditalic")
]

# Text to shape for the context-aware glyphs, and the index of the glyph
SAMPLES = {
    "asterisk.lc": ("*ptr", 0),
    "colon.uc": ("C:", 1),
    "hyphen.lc": ("m-x", 1),
    "plus.lc": ("m+x", 1),
    "x.multiply": ("0xFF", 1),
}

# Text where only the shorter ligature may form, from the DISABLE column of
# pattern.txt: a comment opener must not swallow the second asterisk
COMMENTS = {
    "/**": ["empty.slash_asterisk.liga.0", "slash_asterisk.liga", "asterisk"],
    "**/": ["asterisk", "empty.asterisk_slash.liga.0", "asterisk_slash.liga"],
}

# Text that must stay plain, from the DISABLE column of pattern.txt
PLAIN = [
    "<||>",
    "{|}",
    "[|]",
    ">-<",
    "====",
    "----",
    "######",
    "[->",
    "[==>",
    "M-x",
    "M+x",
]


def text_of(spec):
    return "".join(CHAR_DICT.get(char, char) for char in spec["chars"])


def expected_glyphs(spec):
    """Glyph names a ligature must shape to, cell by cell"""
    cells = len(spec["chars"])
    parts = spec.get("parts") or [None] * (cells - 1) + [spec["name"]]
    return [
        part or "empty.{}.{}".format(spec["name"], i) for i, part in enumerate(parts)
    ]


@unittest.skipUnless(hb, "uharfbuzz is not installed")
@unittest.skipUnless(
    all(path.isfile(font) for font in BUILT_FONTS), "fonts are not built yet"
)
class ShapingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fonts = {}
        for font in BUILT_FONTS:
            face = hb.Face(hb.Blob.from_file_path(font))
            cls.fonts[path.basename(font)] = hb.Font(face)

    def shape(self, font, text):
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(font, buf, {"calt": True})
        return [font.glyph_to_string(info.codepoint) for info in buf.glyph_infos]

    def test_every_ligature_shapes_to_its_glyphs(self):
        """A missing glyph would silently leave the text plain"""
        for name, font in self.fonts.items():
            for spec in LIGATURES:
                if "rule" in spec:
                    continue
                with self.subTest(font=name, text=text_of(spec)):
                    self.assertEqual(
                        self.shape(font, text_of(spec)), expected_glyphs(spec)
                    )

    def test_context_aware_glyphs(self):
        for name, font in self.fonts.items():
            for glyph, (text, index) in SAMPLES.items():
                with self.subTest(font=name, text=text):
                    self.assertEqual(self.shape(font, text)[index], glyph)

    def test_comment_markers_keep_the_extra_asterisk(self):
        for name, font in self.fonts.items():
            for text, glyphs in COMMENTS.items():
                with self.subTest(font=name, text=text):
                    self.assertEqual(self.shape(font, text), glyphs)

    def test_disabled_contexts_stay_plain(self):
        for name, font in self.fonts.items():
            for text in PLAIN:
                with self.subTest(font=name, text=text):
                    for glyph in self.shape(font, text):
                        self.assertNotRegex(glyph, r"^empty\.|\.liga|\.seq|\.lc$|\.uc$")

    def test_built_fonts_are_fixed_pitch(self):
        """macOS only lists the font as monospace with this flag (issue #2)"""
        from fontTools.ttLib import TTFont

        for font in BUILT_FONTS:
            with self.subTest(font=path.basename(font)):
                self.assertEqual(TTFont(font)["post"].isFixedPitch, 1)

    def test_ligatures_are_not_infinite(self):
        """Unlike FiraCode 4+, a longer run than the spec is left alone"""
        for name, font in self.fonts.items():
            for text in ("---->", "<====>", "#####", "||||="):
                with self.subTest(font=name, text=text):
                    for glyph in self.shape(font, text):
                        self.assertNotRegex(glyph, r"^empty\.|\.liga|\.seq")


if __name__ == "__main__":
    unittest.main()
