#!/usr/bin/env python3
"""Tests of the web font build: python3 -m unittest discover -s test"""

import sys
import unittest
from os import path

sys.path.insert(0, path.join(path.dirname(__file__), "..", "src"))

import web  # noqa: E402


class PartitionTest(unittest.TestCase):
    def test_each_code_point_goes_to_one_part(self):
        cps = [0x41, 0x301, 0x103, 0x1EA0, 0x101, 0x3B1, 0x416, 0x2500, 0xE0B0, 0xF0001, 0x1D400]
        parts = dict(web.partition(cps))
        self.assertEqual(parts["latin"], [0x41, 0x301])
        self.assertEqual(parts["vietnamese"], [0x103, 0x1EA0])
        self.assertEqual(parts["latin-ext"], [0x101])
        self.assertEqual(parts["greek"], [0x3B1])
        self.assertEqual(parts["cyrillic"], [0x416])
        self.assertEqual(parts["symbols"], [0x2500])
        self.assertEqual(parts["icons"], [0xE0B0, 0xF0001])
        self.assertEqual(parts["other"], [0x1D400])
        self.assertEqual(sorted(sum(parts.values(), [])), sorted(cps))

    def test_empty_parts_are_left_out(self):
        self.assertEqual(web.partition([0x41, 0x42]), [("latin", [0x41, 0x42])])


class UnicodeRangeTest(unittest.TestCase):
    def test_consecutive_code_points_make_a_range(self):
        self.assertEqual(web.unicode_range([0x41, 0x42, 0x43, 0x45, 0x1EA0, 0x1EA1]), "U+41-43, U+45, U+1EA0-1EA1")


class FontFaceTest(unittest.TestCase):
    def test_a_part_is_limited_to_its_code_points(self):
        rule = web.font_face("Iosevka Dynamo", "fonts/a.latin.woff2?v=1", 700, "italic", [0x41, 0x42])
        self.assertIn('font-family: "Iosevka Dynamo";', rule)
        self.assertIn('src: url("fonts/a.latin.woff2?v=1") format("woff2");', rule)
        self.assertIn("font-weight: 700;", rule)
        self.assertIn("font-style: italic;", rule)
        self.assertIn("unicode-range: U+41-42;", rule)

    def test_a_whole_style_has_no_range(self):
        self.assertNotIn("unicode-range", web.font_face("F", "fonts/a.woff2", 400, "normal"))


if __name__ == "__main__":
    unittest.main()
