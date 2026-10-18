# Iosevka-Dynamo
Adding programming ligatures from [FiraCode](https://github.com/tonsky/FiraCode) to my favorite [Iosevka](https://github.com/be5invis/Iosevka) font.

## Why do I create it?
Although Iosevka has ligatures, but it's not work with my kitty terminal (https://github.com/kovidgoyal/kitty/issues/297).
And FiraCode has some ligatures that I need.

## Which version of font that I use?
* Base font: the latest release of Iosevka, variant `Fixed SS05` (Fira Mono style, no ligatures, no wide glyphs), in Regular, Italic, Oblique, Bold, Bold Italic and Bold Oblique.
* Ligatures: FiraCode v6.2, the latest release, Regular for the regular styles and Bold for the bold ones. Both its glyphs and its `calt` rules are used, so the ligatures behave as in FiraCode, including the arbitrary-length arrows and lines (`-->`, `---->`, `<===>`, `######`, `____`...).

FiraCode 4 had gaps between the pieces of those arrows on kitty (https://github.com/tonsky/FiraCode/issues/1081); kitty has since fixed it by recognizing the `*.seq` glyph names, which this font keeps.

## How does it work?
`scripts/build.sh` downloads both fonts to `assets/`, then runs `src/main.py` once per style:

1. `Patcher` (`src/factory/patcher.py`) opens both fonts with FontForge and scales FiraCode to the em size of Iosevka.
2. It copies the single characters that appear in ligatures (`& ^ ~ \ | : = ! > - < # % . + ? ; / _`) from FiraCode, so they look the same inside and outside a ligature. The asterisk `*` stays from Iosevka.
3. It copies every glyph that the rules of `src/calt.fea` produce and Iosevka does not have: the `*.liga` ligatures, the `*_start.seq`/`*_middle.seq`/`*_end.seq` pieces of arrows and lines, the empty `*.spacer` cells and the context-aware variants (`*ptr`, `m-x`, `0xFF`, `C:`...). Each one is one cell wide. A glyph missing from FiraCode is an error, not a silently dropped ligature.
4. `Generator` (`src/factory/generator.py`) renames the font to `Iosevka Dynamo` and writes the TTF to `build/`. It then sets `post.isFixedPitch` back with fontTools, because FontForge clears it over the zero-width combining marks and macOS would not list the font as monospace otherwise, and compiles `src/calt.fea` with fontTools into the GSUB table that Iosevka already has (`src/features.py`), so Iosevka's own features (`ccmp`, `locl`, `zero`...) stay.

`src/calt.fea` is the `calt` feature of FiraCode 6.2 (SIL Open Font License 1.1) with a few changes, listed at its top: `<<=`, `>>=`, `||=`, `|=`, `.=`, `.-`, `=~` and `!~` are ligatures as in FiraCode 3, although FiraCode 6 dropped or hid them, and the rules that need glyphs Iosevka does not have (Greek, old-style figures, FiraCode's own lowered `l`/`i`/`j`) are left out. Members of its glyph classes that the font lacks are dropped at compile time.

Then the script patches the four main styles with the [Nerd Fonts patcher](https://github.com/ryanoasis/nerd-fonts) Docker image into `Iosevka Dynamo Nerd`, and `src/web.py` converts everything to WOFF2 for the web.

## Requirements
* FontForge with its Python module: `python-fontforge` (Debian/Ubuntu or ArchLinux) or `fontforge` (Gentoo, OpenSUSE).
* The `fontTools` and `brotli` Python modules (`python3-fonttools` and `python3-brotli` on Debian/Ubuntu), for the feature compilation, the fixed-pitch flag and the web fonts.
* `curl`, `unzip` and Docker, for the downloads and the Nerd Fonts patcher.
* The `uharfbuzz` Python module (`pip install uharfbuzz`, it is not packaged by Debian/Ubuntu), only for the shaping tests, which are skipped without it.

## Tests
```sh
python3 -m unittest discover -s test
```
* `test_features.py` compiles a small feature file into a small font and checks the merged GSUB table. With the fonts in `assets/`, it also builds a stand-in of the generated font (upstream Iosevka plus empty FiraCode glyphs plus `calt.fea`) and shapes `test/cases.py` with HarfBuzz against FiraCode 6.2 itself, so the rules are verified without FontForge.
* `test_calt.py` checks `calt.fea` against the FiraCode fonts in `assets/`: it parses, every glyph it produces exists in every style and is one cell wide.
* `test_ligatures.py` shapes the same cases against the built fonts in `build/` and checks the fixed-pitch flag.
* `test_fixedpitch.py` and `test_web.py` cover the fixed-pitch flag and the web font split.

The tests that need `assets/` or `build/` are skipped until `scripts/build.sh` has run, so CI runs the suite before and after the build. `test/pattern.txt` lists the same cases for checking by eye in a terminal.

## Releases
CI builds the fonts on every `v*` tag, on a manual run and once a day. A tag build attaches
`iosevka-dynamo.tar.gz` (every style) and the `iosevka-dynamo-nerd-*.ttf` files to the GitHub
release of that tag. To release, set `FONT_FAMILY_VERSION` in `scripts/build.sh`, move the
`[Unreleased]` entries of `CHANGELOG.md` under the version, and push the tag.

## Use on the web
Every CI build converts the fonts to WOFF2, and the builds from the `main` branch (manual or
daily) publish them to GitHub Pages at https://dynamotn.github.io/Iosevka-Dynamo/, together with
a demo page. The `github-pages` environment only accepts `main`, so a tag build does not deploy
the site itself; the next run on `main` builds the same fonts and does.

Embed the font with a single stylesheet:
```html
<link rel="stylesheet" href="https://dynamotn.github.io/Iosevka-Dynamo/iosevka-dynamo.css">
<style>
  code, pre { font-family: "Iosevka Dynamo", monospace; }
</style>
```

Use `iosevka-dynamo-nerd.css` and the `"Iosevka Dynamo Nerd"` family for Nerd Font icons.

Each style is split by Unicode block (Latin, Vietnamese, Latin Extended, Greek,
Cyrillic, symbols, icons and the rest) and declared with `unicode-range`, so a
browser downloads only the parts a page uses: about 50 KB for English text
instead of the whole 430 KB style. `iosevka-dynamo-full.css` and
`iosevka-dynamo-nerd-full.css` load each style as one file, and the whole
`fonts/<name>.woff2` files stay published.

To build the site locally, run `scripts/build.sh`; the result is written to `public/`.
