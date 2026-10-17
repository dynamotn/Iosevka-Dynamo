"""Mark a generated font as fixed pitch.

FontForge computes ``post.isFixedPitch`` from the glyph advance widths when
it writes a font, and clears it because combining marks have a zero advance.
macOS (CoreText) only treats a font as monospace when that flag is set, so
the generated fonts never showed up as monospace in Terminal, Kitty or
other macOS apps (issue #2). Upstream Iosevka Fixed ships the same zero-width
marks with the flag set, so set it back after FontForge has written the file.
"""

from fontTools.ttLib import TTFont


def mark_fixed_pitch(font_file):
    """Set ``post.isFixedPitch`` of a font file in place.

    Args:
        font_file: (string) Path of the TTF or OTF file to update
    """
    font = TTFont(font_file)
    font["post"].isFixedPitch = 1
    font.save(font_file)
