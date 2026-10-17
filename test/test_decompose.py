#!/usr/bin/env python3
"""Tests of decomposing the ligature font: python3 -m unittest discover -s test"""

import tempfile
import unittest
from os import path

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import Glyph, GlyphComponent

import cases
import decompose  # noqa: E402  (cases puts src/ on the path)


def bounds(font, name):
    pen = BoundsPen(font.getGlyphSet())
    font.getGlyphSet()[name].draw(pen)
    return pen.bounds


def build_font(file_path):
    """A square, and a glyph that is the square mirrored and shifted"""
    pen = TTGlyphPen(None)
    pen.moveTo((100, 0))
    pen.lineTo((400, 0))
    pen.lineTo((400, 300))
    pen.lineTo((100, 300))
    pen.closePath()
    square = pen.glyph()
    component = GlyphComponent()
    component.glyphName = "square"
    component.transform = [[-1, 0], [0, 1]]
    component.x, component.y = 500, 100
    component.flags = 0x0002  # ARGS_ARE_XY_VALUES
    mirrored = Glyph()
    mirrored.numberOfContours = -1
    mirrored.components = [component]
    fb = FontBuilder(1000, isTTF=True)
    fb.setupGlyphOrder([".notdef", "square", "mirrored"])
    fb.setupCharacterMap({0x61: "square", 0x62: "mirrored"})
    fb.setupGlyf(
        {".notdef": TTGlyphPen(None).glyph(), "square": square, "mirrored": mirrored}
    )
    # Left side bearings must match xMin, or fontTools shifts the outlines
    fb.setupHorizontalMetrics(
        {".notdef": (500, 0), "square": (500, 100), "mirrored": (500, 100)}
    )
    fb.setupHorizontalHeader(ascent=800, descent=-200)
    fb.setupNameTable({"familyName": "Test", "styleName": "Regular"})
    fb.setupOS2()
    fb.setupPost()
    fb.save(file_path)


class DecomposeTest(unittest.TestCase):
    def test_keeps_the_drawn_outline(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = path.join(tmp, "source.ttf")
            build_font(source)
            self.assertEqual(decompose.composite_glyphs(TTFont(source)), ["mirrored"])
            before = bounds(TTFont(source), "mirrored")

            target = path.join(tmp, "target.ttf")
            decompose.decompose_file(source, target)

            font = TTFont(target)
            self.assertEqual(decompose.composite_glyphs(font), [])
            self.assertEqual(bounds(font, "mirrored"), before)
            self.assertEqual(bounds(font, "mirrored"), (100, 100, 400, 400))
            self.assertEqual(bounds(font, "square"), (100, 0, 400, 300))


@unittest.skipUnless(
    all(path.isfile(font) for font in cases.FIRACODE.values()),
    "FiraCode fonts are not downloaded to assets/",
)
class FiraCodeDecomposeTest(unittest.TestCase):
    def test_every_glyph_keeps_its_bounds(self):
        for style, font_file in cases.FIRACODE.items():
            with self.subTest(style), tempfile.TemporaryDirectory() as tmp:
                source = TTFont(font_file)
                composites = decompose.composite_glyphs(source)
                self.assertGreater(len(composites), 0)
                before = {name: bounds(source, name) for name in composites}

                target = path.join(tmp, "decomposed.ttf")
                decompose.decompose_file(font_file, target)

                font = TTFont(target)
                self.assertEqual(decompose.composite_glyphs(font), [])
                for name in composites:
                    # Scaled components give fractional bounds; outlines
                    # are rounded to font units
                    for after, original in zip(bounds(font, name), before[name]):
                        self.assertAlmostEqual(after, original, delta=1, msg=name)
                self.assertEqual(font.getGlyphOrder(), source.getGlyphOrder())
                self.assertEqual(font["hmtx"].metrics, source["hmtx"].metrics)


if __name__ == "__main__":
    unittest.main()
