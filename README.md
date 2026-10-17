# Iosevka-Dynamo
Adding programming ligatures from [FiraCode](https://github.com/tonsky/FiraCode) to my favorite [Iosevka](https://github.com/be5invis/Iosevka) font.

## Why do I create it?
Although Iosevka has ligatures, but it's not work with my kitty terminal (https://github.com/kovidgoyal/kitty/issues/297).
And FiraCode has some ligatures that I need.

## Which version of font that I use?
The ligature glyphs come from FiraCode v6.2, the latest release.

Since v4, FiraCode draws arrows and lines (`->`, `==>`, `<=>`, `##`, `__`...) from
`start`/`middle`/`end` pieces with infinite-length rules, which I don't want to use and
which have some bugs on kitty (https://github.com/tonsky/FiraCode/issues/1081).
This font copies the same pieces but keeps its own fixed-length rules, so `-->` is a
ligature and `---->` is not. A few ligatures that FiraCode 6 dropped or made optional
(`|=`, `||=`, `>>=`, `<<=`, `.=`, `.-`) are still built from its glyphs.

## Requirements
This script requires FontForge to build font. AFAIK, you can must `python-fontforge` (Debian/Ubuntu or ArchLinux) or `fontforge` (Gentoo, OpenSUSE).
The web fonts also need the `fontTools` and `brotli` Python modules (`python3-fonttools` and `python3-brotli` on Debian/Ubuntu).

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
