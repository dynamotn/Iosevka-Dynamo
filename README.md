# Iosevka-Dynamo
Adding programming ligatures from [FiraCode](https://github.com/tonsky/FiraCode) to my favorite [Iosevka](https://github.com/be5invis/Iosevka) font.

## Why do I create it?
Although Iosevka has ligatures, but it's not work with my kitty terminal (https://github.com/kovidgoyal/kitty/issues/297).
And FiraCode has some ligatures that I need.

## Which version of font that I use?
FiraCode v4 has infinite-length that I don't want to use and has some bugs on kitty (https://github.com/tonsky/FiraCode/issues/1081).
So I will use FiraCode v3.1 for my font.
> ![NOTE]
> TODO: I will try to get some ligatures in higher version to my font in the future.

## Requirements
This script requires FontForge to build font. AFAIK, you can must `python-fontforge` (Debian/Ubuntu or ArchLinux) or `fontforge` (Gentoo, OpenSUSE).

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

To build the site locally, run `scripts/build.sh`; the result is written to `public/`.
