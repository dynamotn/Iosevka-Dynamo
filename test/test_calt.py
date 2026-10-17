#!/usr/bin/env python3
"""Tests of src/calt.fea against the FiraCode fonts: python3 -m unittest discover -s test

They need the FiraCode fonts in assets/, which scripts/build.sh downloads,
and are skipped until then.
"""

import unittest
from os import path

from fontTools.ttLib import TTFont

import cases
import features  # noqa: E402  (cases puts src/ on the path)


@unittest.skipUnless(
    all(path.isfile(font) for font in cases.FIRACODE.values()),
    "FiraCode fonts are not downloaded to assets/",
)
class CaltFileTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fea = features.read_feature()
        cls.fonts = {style: TTFont(font) for style, font in cases.FIRACODE.items()}

    def test_parses_against_every_style(self):
        for style, font in self.fonts.items():
            with self.subTest(style):
                features.check_feature(self.fea, font.getGlyphOrder())

    def test_every_produced_glyph_exists_in_every_style(self):
        """The patcher copies these; a missing one would lose a ligature"""
        produced = [
            g
            for g in features.glyphs_of(self.fea, include_classes=False)
            if "." in g or "_" in g
        ]
        self.assertGreater(len(produced), 150)
        for style, font in self.fonts.items():
            with self.subTest(style):
                self.assertEqual(sorted(set(produced) - set(font.getGlyphOrder())), [])

    def test_produced_glyphs_are_one_cell_wide(self):
        """Each piece is drawn in its own cell, so none may be scaled"""
        for style, font in self.fonts.items():
            hmtx = font["hmtx"]
            cell = hmtx["m"][0]
            for glyph in features.glyphs_of(self.fea, include_classes=False):
                if glyph in hmtx.metrics and ("." in glyph or "_" in glyph):
                    self.assertEqual(hmtx[glyph][0], cell, "%s in %s" % (glyph, style))

    def test_keeps_the_ligatures_firacode_dropped(self):
        for line in (
            "sub bar'     equal by bar_equal_start.seq;",
            "ignore sub bar' bar equal;",
            "ignore sub less' less equal;",
            "ignore sub greater' greater equal;",
            "sub period.spacer equal' by period_equal.cv32;",
            "sub period.spacer hyphen' by period_hyphen.cv25;",
            "sub equal.spacer asciitilde' by equal_asciitilde.ss07;",
            "sub exclam.spacer asciitilde' by exclam_asciitilde.ss07;",
        ):
            self.assertIn(line, self.fea)

    def test_leaves_firacode_letter_shapes_out(self):
        produced = " ".join(features.glyphs_of(self.fea, include_classes=False))
        for name in ("salt_low", "Greek", "asteriskmath", "tosf"):
            self.assertNotIn(name, produced)

    def test_credits_firacode(self):
        self.assertIn("FiraCode 6.2", self.fea)
        self.assertIn("SIL Open Font License", self.fea)


if __name__ == "__main__":
    unittest.main()
