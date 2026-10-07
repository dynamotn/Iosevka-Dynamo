#!/usr/bin/env python3
"""
Convert built TTF fonts to WOFF2 and generate a static site that can be
hosted on GitHub Pages and embedded with a single stylesheet
"""

import html
import fontforge
from argparse import ArgumentParser
from os import makedirs, path

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


def convert(input_file, output_file):
    """Convert a font file to web font, format is detected by extension"""
    print("Generating '%s'" % output_file)
    font = fontforge.open(input_file)
    try:
        font.generate(output_file)
    finally:
        font.close()


def build_family(family, prefix, input_directory, output_directory, version):
    """Convert all styles of a family to WOFF2 and write its stylesheet

    Returns:
        List of (weight, style) that are available in the family
    """
    query = "?v=%s" % version if version else ""
    faces = []
    rules = []
    for suffix, (weight, style) in STYLES.items():
        file_name = "%s-%s" % (prefix, suffix)
        input_file = path.join(input_directory, file_name + ".ttf")
        if not path.isfile(input_file):
            continue
        convert(input_file, path.join(output_directory, FONTS_DIR, file_name + ".woff2"))
        faces.append((weight, style))
        rules.append(
            "@font-face {\n"
            '  font-family: "%s";\n'
            '  src: url("%s/%s.woff2%s") format("woff2");\n'
            "  font-weight: %d;\n"
            "  font-style: %s;\n"
            "  font-display: swap;\n"
            "}\n" % (family, FONTS_DIR, file_name, query, weight, style)
        )
    if not rules:
        return faces
    with open(path.join(output_directory, prefix + ".css"), "w", encoding="utf-8") as f:
        f.write("\n".join(rules))
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
