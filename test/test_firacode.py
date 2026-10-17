#!/usr/bin/env python3
"""Tests of the ligature specification: python3 -m unittest discover -s test

The glyph tests need the FiraCode fonts in assets/, which scripts/build.sh
downloads; they are skipped until then.
"""

import string
import sys
import unittest
from os import path

sys.path.insert(0, path.join(path.dirname(__file__), "..", "src"))

from factory.firacode import CHAR_DICT, COPY_CHARS, LIGATURES  # noqa: E402

ASSETS_DIR = path.join(path.dirname(__file__), "..", "assets")
FIRACODE_FONTS = [
    path.join(ASSETS_DIR, "FiraCode-%s.ttf" % style) for style in ("Regular", "Bold")
]


def glyphs_of(spec):
    """Glyphs of the ligature font that a spec copies"""
    if spec.get("parts"):
        return [part for part in spec["parts"] if part]
    return [spec["name"]]


def needed_glyphs():
    """Every glyph of the ligature font that the patcher needs"""
    names = set(COPY_CHARS)
    for spec in LIGATURES:
        names.update(glyphs_of(spec))
    return names


class SpecTest(unittest.TestCase):
    def test_names_are_unique(self):
        names = [spec["name"] for spec in LIGATURES]
        self.assertEqual(sorted(names), sorted(set(names)))

    def test_chars_are_known_glyph_names(self):
        known = set(CHAR_DICT) | set(string.ascii_letters)
        for spec in LIGATURES:
            self.assertTrue(spec["chars"], spec["name"])
            for char in spec["chars"]:
                self.assertIn(char, known, spec["name"])

    def test_parts_match_chars(self):
        for spec in LIGATURES:
            if "parts" not in spec:
                continue
            with self.subTest(spec["name"]):
                self.assertEqual(len(spec["parts"]), len(spec["chars"]))
                self.assertTrue(
                    any(spec["parts"]), "a ligature needs at least one drawn part"
                )
                for part in spec["parts"]:
                    self.assertTrue(part is None or isinstance(part, str))

    def test_parts_do_not_need_a_rule(self):
        for spec in LIGATURES:
            if "parts" in spec:
                self.assertNotIn("rule", spec, spec["name"])

    def test_rules_name_their_kind(self):
        for spec in LIGATURES:
            if "rule" in spec:
                self.assertIn("rule_kind", spec, spec["name"])
                self.assertIn("@<{lookup}>", spec["rule"], spec["name"])

    def test_arrows_and_lines_are_built_from_pieces(self):
        """FiraCode 6 no longer has these as one glyph, see firacode.py"""
        for text in ("->", "<-", "=>", "-->", "<=>", "##", "__", "|=", "||="):
            chars = [name for ch in text for name, c in CHAR_DICT.items() if c == ch]
            specs = [spec for spec in LIGATURES if spec["chars"] == chars]
            self.assertEqual(len(specs), 1, text)
            self.assertIn("parts", specs[0], text)


@unittest.skipUnless(
    all(path.isfile(font) for font in FIRACODE_FONTS),
    "FiraCode fonts are not downloaded to assets/",
)
class FiraCodeGlyphTest(unittest.TestCase):
    """Every glyph the specification names must exist, in every style, or the
    patcher would skip the ligature"""

    @classmethod
    def setUpClass(cls):
        from fontTools.ttLib import TTFont

        cls.glyph_orders = {
            path.basename(font): set(TTFont(font).getGlyphOrder())
            for font in FIRACODE_FONTS
        }

    def test_every_needed_glyph_exists(self):
        for font, glyphs in self.glyph_orders.items():
            with self.subTest(font):
                self.assertEqual(sorted(needed_glyphs() - glyphs), [])

    def test_chars_exist(self):
        for font, glyphs in self.glyph_orders.items():
            for spec in LIGATURES:
                for char in spec["chars"]:
                    self.assertIn(char, glyphs, "%s in %s" % (spec["name"], font))

    def test_pieces_are_one_cell_wide(self):
        """Pieces are drawn in their own cell, so none may be scaled"""
        from fontTools.ttLib import TTFont

        for font in FIRACODE_FONTS:
            hmtx = TTFont(font)["hmtx"]
            cell = hmtx["m"][0]
            for spec in LIGATURES:
                for glyph in glyphs_of(spec):
                    self.assertEqual(
                        hmtx[glyph][0], cell, "%s in %s" % (glyph, path.basename(font))
                    )


if __name__ == "__main__":
    unittest.main()
