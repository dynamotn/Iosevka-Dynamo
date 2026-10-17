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
