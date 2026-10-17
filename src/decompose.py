"""Replace the composite glyphs of a TrueType font by their outlines.

FiraCode (TTF since 6.0) builds many ligatures as references to other
glyphs, e.g. ``<|`` is ``|>`` mirrored. FontForge mishandles those when the
font is scaled to another em size and the referenced glyph is copied on its
own, so the ligature font is decomposed with fontTools before FontForge
opens it.
"""

from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont


def composite_glyphs(font):
    """Names of the composite glyphs of a TTFont"""
    glyf = font["glyf"]
    return [name for name in font.getGlyphOrder() if glyf[name].isComposite()]


def decompose(font):
    """Decompose every composite glyph of a TTFont in place"""
    glyph_set = font.getGlyphSet()
    glyf = font["glyf"]
    for name in composite_glyphs(font):
        recording = DecomposingRecordingPen(glyph_set)
        glyph_set[name].draw(recording)
        pen = TTGlyphPen(glyph_set)
        recording.replay(pen)
        glyf[name] = pen.glyph()
    return font


def decompose_file(input_file, output_file):
    """Write a decomposed copy of a TrueType font file"""
    font = TTFont(input_file)
    if "glyf" in font:
        decompose(font)
    font.save(output_file)
