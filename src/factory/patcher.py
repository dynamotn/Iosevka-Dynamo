"""Font patcher to copy the ligature glyphs"""

import fontforge
import psMat

from features import glyphs_of, read_feature

# Characters that appear in ligatures, copied from the ligature font so they
# look the same inside and outside a ligature. The asterisk stays from the
# base font (v1.4.1).
COPY_CHARS = [
    "ampersand",
    "asciicircum",
    "asciitilde",
    "backslash",
    "bar",
    "colon",
    "equal",
    "exclam",
    "greater",
    "hyphen",
    "less",
    "numbersign",
    "percent",
    "period",
    "plus",
    "question",
    "semicolon",
    "slash",
    "underscore",
]


class Patcher(object):
    """Subclass to patch font file to add ligatures

    The glyphs that the contextual alternates of calt.fea produce are copied
    from the ligature font; the rules themselves are compiled into the
    generated file by features.add_calt.
    """

    def __init__(self, base_font, liga_font, fea_text=None):
        """
        Args:
            base_font: (string) Path of base font to create new font
            liga_font: (string) Path of ligature font that want to
                add ligatures to base font
            fea_text: (string) Feature file naming the glyphs to copy,
                calt.fea by default
        """
        try:
            self.base_font = fontforge.open(base_font)
            self.liga_font = fontforge.open(liga_font)

            # Scale ligature font to em size of base font
            self.liga_font.em = self.base_font.em
            # FiraCode (TTF since 6.0) builds many ligatures as references to
            # other glyphs, e.g. <| is |> mirrored. Pasting a reference to a
            # glyph the base font lacks crashes FontForge, so bake them in.
            self.liga_font.selection.all()
            self.liga_font.unlinkReferences()
        except Exception as e:
            print("Exception while opening font file: {}".format(e))
            raise
        self.fea_text = fea_text if fea_text is not None else read_feature()

    def copy_char_from_source(self, name):
        """Copy character from ligature font to FontForge's clipboard

        Args:
            name: (string) Name of character in ligature font.

        Returns:
            True/False: Success or not
        """
        try:
            self.liga_font.selection.none()
            self.liga_font.selection.select(name)
            self.liga_font.copy()
            return True
        except ValueError:
            return False

    def paste_char_to_destination(self, name):
        """Paste character from FontForge's clipboard to base font

        Args:
            name: (string) Name of character in ligature font.
        """
        if name not in self.base_font:
            # Create a new character for ligature
            self.base_font.createChar(-1, name)

        # Paste from FontForge's clipboard
        self.base_font.selection.none()
        self.base_font.selection.select(name)
        self.base_font.paste()

        # Correct width
        self.correct_char_width(self.base_font[name])

    def correct_char_width(self, glyph):
        """Correct the horizontal advance and scale of a ligature/character.

        Args:
            glyph: (FontForge's glyph) Glyph of font
        """
        # Get max width of glyph that ligature must resize to, use m character
        max_width = self.base_font[ord("m")].width
        if glyph.width == max_width:
            return

        print("Correcting width from {}".format(glyph.width))
        # Scale large ligature to standard size
        scale = float(max_width) / glyph.width
        glyph.transform(psMat.scale(scale, 1.0))
        glyph.width = max_width

    def rename_base_char(self, name):
        """Give a glyph of the base font the name the rules use for it, found
        by code point in the ligature font

        Args:
            name: (string) Glyph name in the ligature font

        Returns:
            True/False: whether the base font has the glyph under that name now
        """
        if name in self.base_font:
            return True
        code_point = self.liga_font[name].unicode
        if code_point == -1 or code_point not in self.base_font:
            return False
        print("Renaming {} to {}".format(self.base_font[code_point].glyphname, name))
        self.base_font[code_point].glyphname = name
        return True

    def glyphs_to_copy(self):
        """Glyphs the rules need that the base font has not, in rule order.

        Raises:
            LookupError: a glyph is missing from the ligature font too, so a
                rule could not be compiled.
        """
        names = []
        for name in glyphs_of(self.fea_text, include_classes=False):
            if name in COPY_CHARS:
                names.append(name)
            elif name in self.liga_font:
                if not self.rename_base_char(name):
                    names.append(name)
            elif name not in self.base_font:
                raise LookupError("Glyph {} is missing in both fonts".format(name))
        return names

    def patch(self):
        """Patch font"""
        for name in self.glyphs_to_copy():
            print("Adding {}".format(name))
            if not self.copy_char_from_source(name):
                raise LookupError("Glyph {} is missing in ligature font".format(name))
            self.paste_char_to_destination(name)
