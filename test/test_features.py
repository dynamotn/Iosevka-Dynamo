#!/usr/bin/env python3
"""Tests of compiling calt.fea into a font: python3 -m unittest discover -s test

The last test builds a stand-in of the generated font from the upstream
Iosevka and FiraCode files in assets/ and needs uharfbuzz, so it is skipped
until scripts/build.sh has downloaded them.
"""

import tempfile
import unittest
from os import path

from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from fontTools.fontBuilder import FontBuilder
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import Glyph

import cases
import features  # noqa: E402  (cases puts src/ on the path)

MINI_CALT = """
languagesystem DFLT dflt;
@Lowercase = [a b missing];
feature calt {
  lookup arrows {
    sub [hyphen_start.seq hyphen_middle.seq] hyphen' [hyphen greater] by hyphen_middle.seq;
    sub [hyphen_start.seq hyphen_middle.seq] hyphen' by hyphen_end.seq;
    sub [hyphen_start.seq hyphen_middle.seq] greater' by greater_hyphen_end.seq;
    sub hyphen' [hyphen greater] by hyphen_start.seq;
  } arrows;
  lookup lowercase {
    sub @Lowercase hyphen' @Lowercase by hyphen.lc;
  } lowercase;
} calt;
"""
GLYPHS = [
    ".notdef",
    "space",
    "a",
    "b",
    "c",
    "hyphen",
    "greater",
    "hyphen_start.seq",
    "hyphen_middle.seq",
    "hyphen_end.seq",
    "greater_hyphen_end.seq",
    "hyphen.lc",
]


def build_font(file_path):
    """A tiny TTF with a GSUB feature of its own, like Iosevka has"""
    fb = FontBuilder(1000, isTTF=True)
    fb.setupGlyphOrder(GLYPHS)
    fb.setupCharacterMap(
        {
            0x20: "space",
            0x61: "a",
            0x62: "b",
            0x63: "c",
            0x2D: "hyphen",
            0x3E: "greater",
        }
    )
    fb.setupGlyf({name: Glyph() for name in GLYPHS})
    fb.setupHorizontalMetrics({name: (500, 0) for name in GLYPHS})
    fb.setupHorizontalHeader(ascent=800, descent=-200)
    fb.setupNameTable({"familyName": "Test", "styleName": "Regular"})
    fb.setupOS2()
    fb.setupPost()
    addOpenTypeFeaturesFromString(
        fb.font,
        "languagesystem DFLT dflt; languagesystem latn dflt; feature liga { sub a b by c; } liga;",
    )
    fb.save(file_path)


class FeatureTextTest(unittest.TestCase):
    def test_glyphs_of_lists_names_in_order(self):
        names = features.glyphs_of(
            "lookup x_y {\n  sub a' b by c.liga; # d\n  sub @X e' by \\f;\n} x_y;"
        )
        self.assertEqual(names, ["a", "b", "c.liga", "e", "f"])

    def test_glyphs_of_can_skip_class_members(self):
        text = "@X = [a b];\nsub @X c' by d;"
        self.assertIn("a", features.glyphs_of(text))
        self.assertNotIn("a", features.glyphs_of(text, include_classes=False))
        self.assertIn("d", features.glyphs_of(text, include_classes=False))

    def test_filter_classes_drops_unknown_members(self):
        text = "@A = [a b];\n@B = [@A c];\nsub @B d' by e;"
        self.assertEqual(
            features.filter_classes(text, ["a", "c", "d", "e"]),
            "@A = [a];\n@B = [@A c];\nsub @B d' by e;",
        )

    def test_calt_file_parses(self):
        fea = features.read_feature()
        features.check_feature(fea, features.glyphs_of(fea))


class MergeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.font_file = path.join(self.tmp.name, "test.ttf")
        build_font(self.font_file)
        font = TTFont(self.font_file)
        features.add_features(font, MINI_CALT)
        font.save(self.font_file)
        self.font = TTFont(self.font_file)
        self.gsub = self.font["GSUB"].table

    def tearDown(self):
        self.tmp.cleanup()

    def feature_tags(self):
        return [record.FeatureTag for record in self.gsub.FeatureList.FeatureRecord]

    def test_existing_feature_is_kept_and_list_stays_sorted(self):
        self.assertEqual(self.feature_tags(), ["calt", "liga"])

    def test_every_language_system_gets_the_new_feature(self):
        for lang_sys in features.lang_systems(self.gsub):
            self.assertEqual(sorted(lang_sys.FeatureIndex), [0, 1])
        self.assertEqual(len(self.gsub.ScriptList.ScriptRecord), 2)

    def test_lookups_are_appended_and_references_shifted(self):
        lookups = self.gsub.LookupList.Lookup
        self.assertEqual(lookups[0].LookupType, 4)  # liga comes first
        calt = next(
            r.Feature
            for r in self.gsub.FeatureList.FeatureRecord
            if r.FeatureTag == "calt"
        )
        self.assertEqual(len(calt.LookupListIndex), 2)
        self.assertTrue(all(i >= 1 for i in calt.LookupListIndex))
        for i in calt.LookupListIndex:
            for subtable in lookups[i].SubTable:
                for record in getattr(subtable, "SubstLookupRecord", []):
                    self.assertEqual(lookups[record.LookupListIndex].LookupType, 1)

    @unittest.skipUnless(cases.hb, "uharfbuzz is not installed")
    def test_shaping(self):
        shape = cases.shaper(self.font_file)
        self.assertEqual(shape("ab"), ["c"])
        self.assertEqual(shape("->"), ["hyphen_start.seq", "greater_hyphen_end.seq"])
        self.assertEqual(
            shape("--->"),
            [
                "hyphen_start.seq",
                "hyphen_middle.seq",
                "hyphen_middle.seq",
                "greater_hyphen_end.seq",
            ],
        )
        self.assertEqual(shape("a-b"), ["a", "hyphen.lc", "b"])
        self.assertEqual(shape("- "), ["hyphen", "space"])


@unittest.skipUnless(cases.hb, "uharfbuzz is not installed")
@unittest.skipUnless(
    path.isfile(cases.IOSEVKA) and path.isfile(cases.FIRACODE["Regular"]),
    "fonts are not downloaded to assets/",
)
class StandInFontTest(unittest.TestCase):
    """Upstream Iosevka plus empty stand-ins for the FiraCode glyphs plus
    calt.fea must shape like FiraCode, without needing FontForge"""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        fea = features.read_feature()
        fira = set(TTFont(cases.FIRACODE["Regular"]).getGlyphOrder())
        font = TTFont(cases.IOSEVKA)
        order = font.getGlyphOrder()
        needed = [
            g
            for g in features.glyphs_of(fea, include_classes=False)
            if g in fira and g not in order
        ]
        font.setGlyphOrder(order + needed)
        for name in needed:
            font["glyf"].glyphs[name] = Glyph()
            font["hmtx"].metrics[name] = (500, 0)
        font["maxp"].numGlyphs = len(order) + len(needed)
        font["post"].extraNames = []
        font["post"].mapping = {}
        features.add_features(font, fea)
        cls.font_file = path.join(cls.tmp.name, "standin.ttf")
        font.save(cls.font_file)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_shapes_like_firacode(self):
        ours = cases.shaper(self.font_file)
        fira = cases.shaper(cases.FIRACODE["Regular"])
        for text in cases.TEXTS:
            with self.subTest(text=text):
                self.assertEqual(ours(text), cases.expected(fira, text))

    def test_iosevka_features_are_kept(self):
        tags = {
            r.FeatureTag
            for r in TTFont(self.font_file)["GSUB"].table.FeatureList.FeatureRecord
        }
        self.assertIn("calt", tags)
        self.assertIn("ccmp", tags)

    def test_latin_web_part_keeps_the_ligatures(self):
        """The Latin part of the web font is all a page of code loads"""
        try:
            import brotli  # noqa: F401
        except ImportError:
            self.skipTest("brotli is not installed")
        import web

        cmap = TTFont(self.font_file).getBestCmap()
        latin = dict(web.partition(sorted(cmap)))["latin"]
        woff2 = path.join(self.tmp.name, "latin.woff2")
        web.write_subset(self.font_file, woff2, latin)
        # HarfBuzz does not read WOFF2, unpack it first
        part = TTFont(woff2)
        part.flavor = None
        ttf = path.join(self.tmp.name, "latin.ttf")
        part.save(ttf)

        ours = cases.shaper(ttf)
        fira = cases.shaper(cases.FIRACODE["Regular"])
        for text in cases.TEXTS:
            with self.subTest(text=text):
                self.assertEqual(ours(text), cases.expected(fira, text))


if __name__ == "__main__":
    unittest.main()
