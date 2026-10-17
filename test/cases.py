"""Shared cases of the ligature tests: text to shape, and what this font
does differently from FiraCode 6.2 on purpose (see src/calt.fea)"""

import sys
from os import path

sys.path.insert(0, path.join(path.dirname(__file__), "..", "src"))

ASSETS_DIR = path.join(path.dirname(__file__), "..", "assets")
BUILD_DIR = path.join(path.dirname(__file__), "..", "build")
FIRACODE = {
    style: path.join(ASSETS_DIR, "FiraCode-%s.ttf" % style)
    for style in ("Regular", "Bold")
}
IOSEVKA = path.join(ASSETS_DIR, "IosevkaFixedSS05-Regular.ttf")

try:
    import uharfbuzz as hb
except ImportError:  # pragma: no cover
    hb = None

# Text whose shaping must equal FiraCode's, unless listed in DIFFERENT
TEXTS = [
    # arrows and lines, at any length
    "->",
    "-->",
    "---->",
    "<----",
    "<---->",
    "|----->",
    "<-----|",
    "-----|",
    "=====>",
    "<=====",
    "<=====>",
    "|=====>",
    "<=====|",
    "<<----->>",
    ">>----->",
    "--->>",
    "<<---",
    "==>>",
    "|-----",
    "||-----",
    "/=====",
    "=====/",
    "=:====",
    "====!=",
    "________",
    "########",
    "_____|_",
    # not lines: stay plain however long
    "~~~~>",
    "<~~~~",
    "*****",
    ":::::",
    ">>>>>",
    "<-",
    "<--",
    "<->",
    "<<->>",
    "=>",
    "==>",
    "<==",
    "<=>",
    "<==>",
    "=====",
    "------",
    "######",
    "____",
    "->>",
    ">>-",
    "<<-",
    "-<<",
    "=>>",
    "=<<",
    ">=>",
    "<=<",
    ">->",
    "<-<",
    "-|",
    "|-",
    "||-",
    "|->",
    "<-|",
    "|=>",
    "<=|",
    "_|_",
    "/=",
    "/==",
    "//=",
    "=/=",
    "=:=",
    "=!=",
    "|==",
    "||==",
    ">>==",
    "<<==",
    # kept from FiraCode 3.1
    "|=",
    "||=",
    ">>=",
    "<<=",
    ".=",
    ".-",
    "=~",
    "!~",
    # FiraCode lowers l, i and j here; Iosevka's letters stay
    "Fl",
    "Tl",
    "fi",
    "fj",
    # other ligatures
    "==",
    "===",
    "!=",
    "!==",
    "<=",
    ">=",
    "<>",
    "<~>",
    "~~>",
    "<~~",
    "~>",
    "~@",
    "~-",
    "-~",
    "<|",
    "|>",
    "<|>",
    "<||",
    "||>",
    "<|||",
    "|||>",
    "||",
    "|||",
    "<$",
    "$>",
    "<$>",
    "<+",
    "+>",
    "<+>",
    "<*",
    "*>",
    "<*>",
    "</",
    "/>",
    "</>",
    "<!--",
    "www",
    "::",
    ":::",
    ":=",
    "::=",
    "..",
    "...",
    "..=",
    "..<",
    "!!",
    "!!.",
    "?.",
    "??",
    "?=",
    ".?",
    "++",
    "+++",
    "**",
    "***",
    "*/",
    "/*",
    "//",
    "///",
    "&&",
    "%%",
    ";;",
    "~~",
    "^=",
    "#{",
    "#[",
    "#(",
    "#?",
    "#:",
    "#=",
    "#!",
    "#_",
    "#_(",
    "]#",
    "{|",
    "|}",
    "[|",
    "|]",
    "/\\",
    "\\/",
    ":>",
    "<:",
    ">:",
    ":<",
    # context-aware glyphs
    "0xFF",
    "1920x1080",
    "m-x",
    "M-x",
    "m+x",
    "M+x",
    "*ptr",
    "*HA",
    "C:",
    "e:",
    # contexts that FiraCode disables
    "<||>",
    "{|}",
    "[|]",
    "/**",
    "**/",
    "||||",
    "<<<<",
    ">>>>",
    ":>=",
    ">:>",
    "=<",
    "=/",
    "a:b",
    "<:<",
    ":>:",
]

# Text -> glyphs, where this font differs from FiraCode 6.2 on purpose
DIFFERENT = {
    "|=": ["bar_equal_start.seq", "equal_end.seq"],
    "||=": ["bar.spacer", "bar_bar_equal_start.seq", "equal_end.seq"],
    ">>=": ["greater.spacer", "greater_greater_equal_start.seq", "equal_end.seq"],
    "<<=": ["less.spacer", "less_less_equal_start.seq", "equal_end.seq"],
    ".=": ["period.spacer", "period_equal.cv32"],
    ".-": ["period.spacer", "period_hyphen.cv25"],
    "=~": ["equal.spacer", "equal_asciitilde.ss07"],
    "!~": ["exclam.spacer", "exclam_asciitilde.ss07"],
    "Fl": ["F", "l"],
    "Tl": ["T", "l"],
    "fi": ["f", "i"],
    "fj": ["f", "j"],
}


def shaper(font_file):
    """A function shaping text with HarfBuzz to a list of glyph names"""
    font = hb.Font(hb.Face(hb.Blob.from_file_path(font_file)))

    def shape(text):
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(font, buf, {"calt": True})
        return [font.glyph_to_string(info.codepoint) for info in buf.glyph_infos]

    return shape


def expected(fira_shape, text):
    return DIFFERENT.get(text) or fira_shape(text)
