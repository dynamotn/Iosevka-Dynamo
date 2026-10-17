#!/usr/bin/env python3
"""End-to-end tests of the built fonts: python3 -m unittest discover -s test

They shape text with HarfBuzz against build/iosevka-dynamo-*.ttf and compare
it with the FiraCode fonts in assets/, so they need the uharfbuzz module and
a previous run of scripts/build.sh; they are skipped until then.
"""

import unittest
from os import path

from fontTools.ttLib import TTFont

import cases

# Built style -> FiraCode style its ligatures come from
BUILT_FONTS = {
    path.join(cases.BUILD_DIR, "iosevka-dynamo-%s.ttf" % style): fira
    for style, fira in (
        ("regular", "Regular"),
        ("italic", "Regular"),
        ("bold", "Bold"),
        ("bolditalic", "Bold"),
    )
}


@unittest.skipUnless(cases.hb, "uharfbuzz is not installed")
@unittest.skipUnless(
    all(path.isfile(font) for font in BUILT_FONTS)
    and all(path.isfile(f) for f in cases.FIRACODE.values()),
    "fonts are not built yet",
)
class BuiltFontTest(unittest.TestCase):
    def test_shapes_like_firacode(self):
        """A glyph missing from the font would silently leave the text plain"""
        for built, fira_style in BUILT_FONTS.items():
            ours = cases.shaper(built)
            fira = cases.shaper(cases.FIRACODE[fira_style])
            for text in cases.TEXTS:
                with self.subTest(font=path.basename(built), text=text):
                    self.assertEqual(ours(text), cases.expected(fira, text))

    def test_copied_glyphs_keep_firacode_proportions(self):
        """Each copied glyph is FiraCode's, scaled to Iosevka's em and cell"""
        from fontTools.pens.boundsPen import BoundsPen

        def bounds(font, name):
            pen = BoundsPen(font.getGlyphSet())
            font.getGlyphSet()[name].draw(pen)
            return pen.bounds

        for built, fira_style in BUILT_FONTS.items():
            ours, fira = TTFont(built), TTFont(cases.FIRACODE[fira_style])
            scale_y = ours["head"].unitsPerEm / fira["head"].unitsPerEm
            scale_x = ours["hmtx"]["m"][0] / fira["hmtx"]["m"][0]
            copied = [
                g
                for g in ours.getGlyphOrder()
                if g in fira.getGlyphOrder() and ("." in g or "_" in g)
            ]
            self.assertGreater(len(copied), 150)
            for name in copied:
                expected = bounds(fira, name)
                if expected is None:
                    continue
                with self.subTest(font=path.basename(built), glyph=name):
                    xmin, ymin, xmax, ymax = expected
                    want = (
                        xmin * scale_x,
                        ymin * scale_y,
                        xmax * scale_x,
                        ymax * scale_y,
                    )
                    for got, exp in zip(bounds(ours, name), want):
                        self.assertAlmostEqual(got, exp, delta=4)

    def test_fixed_pitch(self):
        """macOS only lists the font as monospace with this flag (issue #2)"""
        for built in BUILT_FONTS:
            with self.subTest(font=path.basename(built)):
                self.assertEqual(TTFont(built)["post"].isFixedPitch, 1)

    def test_iosevka_features_are_kept(self):
        for built in BUILT_FONTS:
            tags = {
                r.FeatureTag
                for r in TTFont(built)["GSUB"].table.FeatureList.FeatureRecord
            }
            self.assertIn("calt", tags)
            self.assertIn("ccmp", tags)


if __name__ == "__main__":
    unittest.main()
