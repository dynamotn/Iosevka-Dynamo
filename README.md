# Iosevka-Dynamo
Adding programming ligatures from [FiraCode](https://github.com/tonsky/FiraCode) to my favorite [Iosevka](https://github.com/be5invis/Iosevka) font.

## Why do I create it?
Although Iosevka has ligatures, but it's not work with my kitty terminal (https://github.com/kovidgoyal/kitty/issues/297).
And FiraCode has some ligatures that I need.

## Which version of font that I use?
* Base font: the latest release of Iosevka, variant `Fixed SS05` (Fira Mono style, no ligatures, no wide glyphs), in Regular, Italic, Oblique, Bold, Bold Italic and Bold Oblique.
* Ligature glyphs: FiraCode v6.2, the latest release, Regular for the regular styles and Bold for the bold ones.

## How does it work?
`scripts/build.sh` downloads both fonts to `assets/`, then runs `src/main.py` once per style:

1. `Patcher` (`src/factory/patcher.py`) opens both fonts with FontForge and scales FiraCode to the em size of Iosevka.
2. It copies the single characters that appear in ligatures (`& ^ ~ \ | : = ! > - < # % . + ? ; / _`) from FiraCode, so they look the same inside and outside a ligature. The asterisk `*` stays from Iosevka.
3. For each entry of `LIGATURES` in `src/factory/firacode.py`, it copies the FiraCode glyph(s) by name and writes its own `calt` rules: every character of the sequence is substituted by one glyph per cell, so the font stays monospaced and the sequence has a fixed length.
   * A plain ligature (`==`, `<|>`, `www`...) draws the FiraCode `*.liga` glyph in the cell of the last character and empty glyphs in the others.
   * Arrows and lines (`->`, `==>`, `<=>`, `##`, `__`...) have a `parts` list: since v4, FiraCode draws them from `*_start.seq`, `*_middle.seq` and `*_end.seq` pieces with infinite-length rules, which I don't want to use and which have some bugs on kitty (https://github.com/tonsky/FiraCode/issues/1081). This font copies the same pieces, one per cell, but keeps fixed-length rules: `-->` is a ligature and `---->` is not.
   * A few ligatures that FiraCode 6 dropped or made optional are kept: `|=`, `||=`, `>>=`, `<<=` are built from its pieces, `.=` and `.-` come from its `cv32`/`cv25` variants, and `:>`, `<:`, `>:`, `:<` use its vertically centered glyphs.
   * Context-aware glyphs (`*ptr`, `m-x`, `m+x`, `0xFF`, `C:`) use a custom rule instead of a sequence, and `ignore_before`/`ignore_after` disable a ligature in contexts such as `/**`, `>-<` or `<||>`.
   * A glyph missing from FiraCode is an error, not a silently dropped ligature.
4. `Generator` (`src/factory/generator.py`) renames the font to `Iosevka Dynamo`, writes the TTF to `build/` and sets `post.isFixedPitch` back with fontTools, because FontForge clears it over the zero-width combining marks and macOS would not list the font as monospace otherwise.

Then the script patches the four main styles with the [Nerd Fonts patcher](https://github.com/ryanoasis/nerd-fonts) Docker image into `Iosevka Dynamo Nerd`, and `src/web.py` converts everything to WOFF2 for the web.

## Requirements
* FontForge with its Python module: `python-fontforge` (Debian/Ubuntu or ArchLinux) or `fontforge` (Gentoo, OpenSUSE).
* The `fontTools` and `brotli` Python modules (`python3-fonttools` and `python3-brotli` on Debian/Ubuntu), for the fixed-pitch flag and the web fonts.
* `curl`, `unzip` and Docker, for the downloads and the Nerd Fonts patcher.
* The `uharfbuzz` Python module (`python3-uharfbuzz`), only for the end-to-end tests.

## Tests
```sh
python3 -m unittest discover -s test
```
The tests of the ligature specification check that every glyph it names exists in the FiraCode fonts in `assets/`, and the end-to-end tests shape every ligature, the disabled contexts and the fixed-pitch flag against the fonts in `build/` with HarfBuzz. Both are skipped until `scripts/build.sh` has run, so CI runs the suite before and after the build. `test/pattern.txt` lists the same cases for checking by eye in a terminal.

## Use on the web
Every CI build converts the fonts to WOFF2 and publishes them to GitHub Pages at
https://dynamotn.github.io/Iosevka-Dynamo/, together with a demo page.

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
