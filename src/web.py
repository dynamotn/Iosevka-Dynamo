#!/usr/bin/env python3
"""
Convert built TTF fonts to WOFF2 and generate a static site that can be
hosted on GitHub Pages and embedded with a single stylesheet

Each style is also split by Unicode block into small WOFF2 files, declared
with `unicode-range`, so a browser only downloads the parts a page uses.
"""

import html
from argparse import ArgumentParser
from os import makedirs, path

from fontTools import subset
from fontTools.ttLib import TTFont

FONTS_DIR = "fonts"

# Style suffix of file name -> (font-weight, font-style)
STYLES = {
    "regular": (400, "normal"),
    "italic": (400, "italic"),
    "oblique": (400, "oblique"),
    "bold": (700, "normal"),
    "bolditalic": (700, "italic"),
    "boldoblique": (700, "oblique"),
}

# Font family name -> prefix of file name
FAMILIES = {
    "Iosevka Dynamo": "iosevka-dynamo",
    "Iosevka Dynamo Nerd": "iosevka-dynamo-nerd",
}

# Parts of each style, in order: a code point goes to the first part whose
# blocks hold it, and the ones of no part go to "other". Combining marks stay
# with Latin, so a letter and its accent are drawn by one font.
SUBSETS = [
    (
        "latin",
        [
            (0x0000, 0x00FF),
            (0x0131, 0x0131),
            (0x0152, 0x0153),
            (0x02BB, 0x02BC),
            (0x02C6, 0x02C6),
            (0x02DA, 0x02DA),
            (0x02DC, 0x02DC),
            (0x0300, 0x036F),
            (0x2000, 0x206F),
            (0x20AC, 0x20AC),
            (0x2122, 0x2122),
            (0x2190, 0x2199),
            (0x2212, 0x2215),
            (0xFEFF, 0xFEFF),
            (0xFFFD, 0xFFFD),
        ],
    ),
    (
        "vietnamese",
        [
            (0x0102, 0x0103),
            (0x0110, 0x0111),
            (0x0128, 0x0129),
            (0x0168, 0x0169),
            (0x01A0, 0x01A1),
            (0x01AF, 0x01B0),
            (0x1EA0, 0x1EF9),
            (0x20AB, 0x20AB),
        ],
    ),
    (
        "latin-ext",
        [
            (0x0100, 0x02FF),
            (0x1D00, 0x1DBF),
            (0x1E00, 0x1EFF),
            (0x20A0, 0x20CF),
            (0x2C60, 0x2C7F),
            (0xA720, 0xA7FF),
        ],
    ),
    ("greek", [(0x0370, 0x03FF), (0x1F00, 0x1FFF)]),
    ("cyrillic", [(0x0400, 0x052F), (0x1C80, 0x1C8F), (0x2DE0, 0x2DFF), (0xA640, 0xA69F)]),
    # Letterlike symbols, arrows, maths, technical, box drawing, shapes, dingbats.
    ("symbols", [(0x2100, 0x2BFF)]),
    # Private use areas, where Nerd Fonts keep their icons.
    ("icons", [(0xE000, 0xF8FF), (0xF0000, 0x10FFFF)]),
]
OTHER = "other"


def parse_args():
    """Parse arguments from command line"""
    parser = ArgumentParser()
    parser.add_argument(
        "input_directory",
        type=str,
        metavar="PATH",
        help="The directory that contains built TTF fonts.",
    )
    parser.add_argument(
        "output_directory",
        type=str,
        metavar="PATH",
        help="The directory to save web fonts, stylesheets and demo page in.",
    )
    parser.add_argument(
        "--version", "-v", type=str, default="", help="Version of fonts."
    )
    parser.add_argument(
        "--base-url",
        "-u",
        type=str,
        default="",
        help="Public URL of the site, used in embed snippets of demo page.",
    )
    parser.add_argument(
        "--sample",
        "-s",
        type=str,
        default="",
        help="Text file to show as ligature sample in demo page.",
    )
    return parser.parse_args()


def partition(codepoints):
    """Split code points into the parts of SUBSETS, then "other"

    Returns:
        List of (name, sorted code points), without empty parts
    """
    parts = {name: [] for name, _ in SUBSETS}
    parts[OTHER] = []
    for cp in sorted(codepoints):
        name = next(
            (n for n, blocks in SUBSETS if any(lo <= cp <= hi for lo, hi in blocks)),
            OTHER,
        )
        parts[name].append(cp)
    return [(name, cps) for name, cps in parts.items() if cps]


def unicode_range(codepoints):
    """CSS `unicode-range` of sorted code points, consecutive ones as ranges"""
    ranges = []
    for cp in codepoints:
        if ranges and cp == ranges[-1][1] + 1:
            ranges[-1][1] = cp
        else:
            ranges.append([cp, cp])
    return ", ".join(
        "U+%X" % lo if lo == hi else "U+%X-%X" % (lo, hi) for lo, hi in ranges
    )


def convert(input_file, output_file):
    """Convert a whole font to WOFF2"""
    print("Generating '%s'" % output_file)
    font = TTFont(input_file)
    font.flavor = "woff2"
    font.save(output_file)
    font.close()


def write_subset(input_file, output_file, codepoints):
    """Write the part of a font that draws the code points, as WOFF2

    Every OpenType feature is kept, and with it every glyph a substitution
    can reach, so ligatures of the part still form.
    """
    print("Generating '%s'" % output_file)
    options = subset.Options()
    options.flavor = "woff2"
    options.layout_features = ["*"]
    options.name_IDs = ["*"]
    options.name_languages = ["*"]
    options.notdef_outline = True
    # Without glyph names Chromium draws the glyphs a little differently.
    options.glyph_names = True
    # FontForge's own tables, which browsers never read.
    options.drop_tables += ["FFTM", "PfEd"]
    font = subset.load_font(input_file, options)
    subsetter = subset.Subsetter(options)
    subsetter.populate(unicodes=codepoints)
    subsetter.subset(font)
    subset.save_font(font, output_file, options)
    font.close()


def font_face(family, url, weight, style, codepoints=None):
    """A @font-face rule, limited to the code points when given"""
    return (
        "@font-face {\n"
        '  font-family: "%s";\n'
        '  src: url("%s") format("woff2");\n'
        "  font-weight: %d;\n"
        "  font-style: %s;\n"
        "  font-display: swap;\n"
        "%s"
        "}\n"
        % (
            family,
            url,
            weight,
            style,
            "  unicode-range: %s;\n" % unicode_range(codepoints) if codepoints else "",
        )
    )


def build_family(family, prefix, input_directory, output_directory, version):
    """Convert all styles of a family to WOFF2 and write its stylesheets

    The family's stylesheet loads the parts of each style by unicode-range;
    `<prefix>-full.css` keeps loading each style as one file.

    Returns:
        List of (weight, style) that are available in the family
    """
    query = "?v=%s" % version if version else ""
    faces = []
    rules = []
    full_rules = []
    for suffix, (weight, style) in STYLES.items():
        file_name = "%s-%s" % (prefix, suffix)
        input_file = path.join(input_directory, file_name + ".ttf")
        if not path.isfile(input_file):
            continue
        # The whole style stays published, for pages that link to it directly.
        convert(input_file, path.join(output_directory, FONTS_DIR, file_name + ".woff2"))
        full_rules.append(
            font_face(family, "%s/%s.woff2%s" % (FONTS_DIR, file_name, query), weight, style)
        )
        with TTFont(input_file) as font:
            codepoints = font.getBestCmap().keys()
        for name, part in partition(codepoints):
            part_name = "%s.%s.woff2" % (file_name, name)
            write_subset(input_file, path.join(output_directory, FONTS_DIR, part_name), part)
            rules.append(
                font_face(family, "%s/%s%s" % (FONTS_DIR, part_name, query), weight, style, part)
            )
        faces.append((weight, style))
    if not rules:
        return faces
    with open(path.join(output_directory, prefix + ".css"), "w", encoding="utf-8") as f:
        f.write("\n".join(rules))
    with open(path.join(output_directory, prefix + "-full.css"), "w", encoding="utf-8") as f:
        f.write("\n".join(full_rules))
    return faces


def build_index(families, output_directory, version, base_url, sample):
    """Write demo page with embed snippets and samples of all styles"""
    sections = []
    for family, faces in families.items():
        prefix = FAMILIES[family]
        css_url = "%s/%s.css" % (base_url.rstrip("/"), prefix) if base_url else prefix + ".css"
        snippet = html.escape(
            '<link rel="stylesheet" href="%s">\n\n'
            "code, pre {\n"
            '  font-family: "%s", monospace;\n'
            "}" % (css_url, family)
        )
        samples = "".join(
            '<p style="font-weight: %d; font-style: %s">%s %d %s'
            " &mdash; -&gt; =&gt; != === &lt;= &gt;= &lt;!-- --&gt; www 0xFF</p>\n"
            % (weight, style, html.escape(family), weight, style)
            for weight, style in faces
        )
        sections.append(
            '<section style="font-family: \'%s\', monospace">\n'
            "<h2>%s</h2>\n<pre><code>%s</code></pre>\n%s</section>\n"
            % (family, html.escape(family), snippet, samples)
        )
    links = "".join(
        '<link rel="stylesheet" href="%s.css">\n' % FAMILIES[family] for family in families
    )
    sample_block = ""
    if sample:
        with open(sample, encoding="utf-8") as f:
            sample_block = (
                '<h2>Ligatures</h2>\n<pre style="font-family: \'Iosevka Dynamo\', monospace">'
                "%s</pre>\n" % html.escape(f.read())
            )
    page = (
        "<!doctype html>\n"
        '<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        "<title>Iosevka Dynamo</title>\n%s"
        "<style>\n"
        "body { margin: 0 auto; max-width: 64rem; padding: 1rem;"
        " font-family: system-ui, sans-serif; color: #222; background: #fff; }\n"
        "pre { overflow-x: auto; padding: 1rem; background: #f4f4f4; }\n"
        "@media (prefers-color-scheme: dark) {\n"
        "  body { color: #ddd; background: #111; }\n"
        "  pre { background: #1d1d1d; }\n"
        "}\n"
        "</style>\n</head>\n<body>\n"
        "<h1>Iosevka Dynamo %s</h1>\n"
        '<p>Source: <a href="https://github.com/dynamotn/Iosevka-Dynamo">'
        "github.com/dynamotn/Iosevka-Dynamo</a></p>\n"
        "%s%s</body>\n</html>\n"
        % (links, html.escape(version), "".join(sections), sample_block)
    )
    with open(path.join(output_directory, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)


def main(input_directory, output_directory, version, base_url, sample):
    makedirs(path.join(output_directory, FONTS_DIR), exist_ok=True)
    families = {}
    for family, prefix in FAMILIES.items():
        faces = build_family(family, prefix, input_directory, output_directory, version)
        if faces:
            families[family] = faces
    if not families:
        raise SystemExit("No font found in '%s'" % input_directory)
    build_index(families, output_directory, version, base_url, sample)
    # Serve files as is, without Jekyll processing on GitHub Pages
    open(path.join(output_directory, ".nojekyll"), "w").close()


if __name__ == "__main__":
    main(**vars(parse_args()))
