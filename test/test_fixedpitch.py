#!/usr/bin/env python3
"""Tests of the fixed-pitch flag fix: python3 -m unittest discover -s test"""

import sys
import tempfile
import unittest
from os import path

from fontTools.fontBuilder import FontBuilder
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import Glyph

sys.path.insert(0, path.join(path.dirname(__file__), "..", "src"))

import fixedpitch  # noqa: E402


def build_font(file_path):
    """Write a tiny TTF like FontForge does: one advance width for every
    visible glyph, zero width for combining marks, and isFixedPitch unset."""
    fb = FontBuilder(1000, isTTF=True)
    fb.setupGlyphOrder([".notdef", "a", "gravecomb"])
    fb.setupCharacterMap({0x61: "a", 0x300: "gravecomb"})
    fb.setupGlyf({name: Glyph() for name in fb.font.getGlyphOrder()})
    fb.setupHorizontalMetrics({".notdef": (500, 0), "a": (500, 0), "gravecomb": (0, 0)})
    fb.setupHorizontalHeader(ascent=800, descent=-200)
    fb.setupNameTable({"familyName": "Test", "styleName": "Regular"})
    fb.setupOS2()
    fb.setupPost(isFixedPitch=0)
    fb.save(file_path)


class MarkFixedPitchTest(unittest.TestCase):
    def test_sets_post_is_fixed_pitch(self):
        with tempfile.TemporaryDirectory() as tmp:
            font_file = path.join(tmp, "test.ttf")
            build_font(font_file)
            self.assertEqual(TTFont(font_file)["post"].isFixedPitch, 0)

            fixedpitch.mark_fixed_pitch(font_file)

            font = TTFont(font_file)
            self.assertEqual(font["post"].isFixedPitch, 1)

    def test_keeps_zero_width_marks(self):
        with tempfile.TemporaryDirectory() as tmp:
            font_file = path.join(tmp, "test.ttf")
            build_font(font_file)

            fixedpitch.mark_fixed_pitch(font_file)

            metrics = TTFont(font_file)["hmtx"].metrics
            self.assertEqual(metrics["a"][0], 500)
            self.assertEqual(metrics["gravecomb"][0], 0)


if __name__ == "__main__":
    unittest.main()
