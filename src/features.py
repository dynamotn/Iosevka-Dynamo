"""Add the contextual alternates of src/calt.fea to a generated font.

The feature file is FiraCode's own ``calt``, so the ligatures behave as in
FiraCode: arrows and lines are built from start/middle/end pieces at any
length. fontTools compiles it and the resulting lookups are merged into the
GSUB table that Iosevka already has, which FontForge kept.
"""

import re
from io import StringIO
from os import path

from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from fontTools.feaLib.parser import Parser
from fontTools.ttLib import TTFont

CALT_FILE = path.join(path.dirname(path.abspath(__file__)), "calt.fea")


def read_feature(fea_file=CALT_FILE):
    with open(fea_file, encoding="utf-8") as f:
        return f.read()


KEYWORDS = {
    "sub",
    "by",
    "ignore",
    "pos",
    "lookup",
    "feature",
    "languagesystem",
    "script",
    "language",
}


def glyphs_of(fea_text, include_classes=True):
    """Glyph names a feature file mentions, in file order. Without
    include_classes the members of class definitions are left out: they are
    the context of rules, not glyphs the rules produce"""
    text = strip_comments(fea_text)
    if not include_classes:
        text = re.sub(r"^@\w+ = \[[^\]]*\];", "", text, flags=re.M)
    # Lookup and feature names, language systems
    text = re.sub(
        r"^\s*(lookup|feature) \S+ \{|^\s*\} \S+;|^\s*languagesystem [^;]*;",
        "",
        text,
        flags=re.M,
    )
    names = []
    seen = set()
    for token in re.findall(r"(?<![@\w.\-])\\?[A-Za-z_.][A-Za-z0-9_.\-]*", text):
        token = token.lstrip("\\")
        if token not in seen and token not in KEYWORDS:
            seen.add(token)
            names.append(token)
    return names


def strip_comments(fea_text):
    return re.sub(r"#[^\n]*", "", fea_text)


def filter_classes(fea_text, glyph_names):
    """Drop the members of each glyph class that the font does not have, so
    the file compiles against a font with fewer glyphs than FiraCode"""
    glyph_names = set(glyph_names)

    def keep(match):
        members = match.group(2).split()
        kept = [m for m in members if m.startswith("@") or m in glyph_names]
        return "%s = [%s];" % (match.group(1), " ".join(kept))

    return re.sub(r"^(@\w+) = \[([^\]]*)\];", keep, fea_text, flags=re.M)


def check_feature(fea_text, glyph_names):
    """Parse the feature file against a glyph set, raising on an unknown glyph"""
    return Parser(StringIO(fea_text), glyphNames=set(glyph_names)).parse()


def shift_lookup_indices(obj, offset, _seen=None):
    """Add offset to every nested lookup reference of a GSUB lookup"""
    if _seen is None:
        _seen = set()
    if id(obj) in _seen:
        return
    _seen.add(id(obj))
    if isinstance(obj, (list, tuple)):
        for item in obj:
            shift_lookup_indices(item, offset, _seen)
    elif hasattr(obj, "__dict__"):
        if hasattr(obj, "SequenceIndex") and hasattr(obj, "LookupListIndex"):
            obj.LookupListIndex += offset
        for value in vars(obj).values():
            shift_lookup_indices(value, offset, _seen)


def merge_gsub(dst, src):
    """Append the lookups and features of GSUB table src to table dst, and
    enable the new features for every script and language of dst"""
    offset = len(dst.LookupList.Lookup)
    for lookup in src.LookupList.Lookup:
        shift_lookup_indices(lookup, offset)
        dst.LookupList.Lookup.append(lookup)
    dst.LookupList.LookupCount = len(dst.LookupList.Lookup)

    new_indices = []
    for record in src.FeatureList.FeatureRecord:
        record.Feature.LookupListIndex = [
            i + offset for i in record.Feature.LookupListIndex
        ]
        record.Feature.LookupCount = len(record.Feature.LookupListIndex)
        dst.FeatureList.FeatureRecord.append(record)
        new_indices.append(len(dst.FeatureList.FeatureRecord) - 1)

    for lang_sys in lang_systems(dst):
        lang_sys.FeatureIndex.extend(new_indices)
        lang_sys.FeatureCount = len(lang_sys.FeatureIndex)

    sort_features(dst)


def lang_systems(gsub):
    for script in gsub.ScriptList.ScriptRecord:
        if script.Script.DefaultLangSys is not None:
            yield script.Script.DefaultLangSys
        for record in script.Script.LangSysRecord:
            yield record.LangSys


def sort_features(gsub):
    """Keep the feature list sorted by tag, as OpenType requires"""
    records = gsub.FeatureList.FeatureRecord
    order = sorted(range(len(records)), key=lambda i: (records[i].FeatureTag, i))
    remap = {old: new for new, old in enumerate(order)}
    gsub.FeatureList.FeatureRecord = [records[i] for i in order]
    gsub.FeatureList.FeatureCount = len(records)
    for lang_sys in lang_systems(gsub):
        lang_sys.FeatureIndex = sorted(remap[i] for i in lang_sys.FeatureIndex)
        if lang_sys.ReqFeatureIndex != 0xFFFF:
            lang_sys.ReqFeatureIndex = remap[lang_sys.ReqFeatureIndex]


def add_features(font, fea_text):
    """Compile fea_text and merge its GSUB into the GSUB of a TTFont"""
    fea_text = filter_classes(fea_text, font.getGlyphOrder())
    compiled = TTFont()
    compiled.setGlyphOrder(font.getGlyphOrder())
    addOpenTypeFeaturesFromString(compiled, fea_text, tables=["GSUB"])
    if "GSUB" in font:
        merge_gsub(font["GSUB"].table, compiled["GSUB"].table)
    else:
        font["GSUB"] = compiled["GSUB"]


def add_calt(font_file, fea_file=CALT_FILE):
    """Add the contextual alternates to a font file in place"""
    font = TTFont(font_file)
    add_features(font, read_feature(fea_file))
    font.save(font_file)
