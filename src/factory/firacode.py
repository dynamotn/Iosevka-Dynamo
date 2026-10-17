"""Specification of font ligatures from FiraCode 6.2

Each entry of LIGATURES names the glyph(s) to copy from FiraCode for a
sequence of characters:

* ``chars``: the input characters, by glyph name.
* ``name``: a glyph of FiraCode. Without ``parts`` it is a single ligature
  glyph drawn in the cell of the last character, while the other cells are
  replaced by empty glyphs.
* ``parts``: one glyph of FiraCode per character, for the ligatures that
  FiraCode 4+ builds from ``*_start.seq``, ``*_middle.seq`` and ``*_end.seq``
  pieces (arrows, lines, ``##``, ``__``...). ``None`` keeps a cell empty. The
  sequence stays fixed-length: longer runs are left alone, unlike FiraCode.
* ``rule``/``rule_kind``: a custom contextual rule, for context-aware glyphs.
* ``ignore_before``/``ignore_after``: contexts that disable the ligature.
"""

import string

CHAR_DICT = {
    "ampersand": "&",
    "asciicircum": "^",
    "asciitilde": "~",
    "asterisk": "*",
    "backslash": "\\",
    "bar": "|",
    "colon": ":",
    "equal": "=",
    "exclam": "!",
    "greater": ">",
    "hyphen": "-",
    "less": "<",
    "numbersign": "#",
    "percent": "%",
    "period": ".",
    "plus": "+",
    "question": "?",
    "semicolon": ";",
    "slash": "/",
    "underscore": "_",
    "at": "@",
    "braceleft": "{",
    "braceright": "}",
    "bracketleft": "[",
    "bracketright": "]",
    "dollar": "$",
    "parenleft": "(",
    "parenright": ")",
    "w": "w",
    "x": "x",
}
DIGIT = "zero one two three four five six seven eight nine"
SPACE = "space"
HEX_DIGIT = DIGIT + " a b c d e f A B C D E F"
BRACKET = "bracketleft bracketright braceleft braceright parenleft parenright"
LOWERCASE = " ".join(list(string.ascii_lowercase))
UPPERCASE = " ".join(list(string.ascii_uppercase))
TALL = UPPERCASE + " " + DIGIT + " " + BRACKET + " bar"
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
LIGATURES = [
    {  # &&
        "chars": ["ampersand", "ampersand"],
        "name": "ampersand_ampersand.liga",
    },
    {  # ^=
        "chars": ["asciicircum", "equal"],
        "name": "asciicircum_equal.liga",
    },
    {  # ~~
        "chars": ["asciitilde", "asciitilde"],
        "name": "asciitilde_asciitilde.liga",
    },
    {  # ~~>
        "chars": ["asciitilde", "asciitilde", "greater"],
        "name": "asciitilde_asciitilde_greater.liga",
    },
    {  # ~@
        "chars": ["asciitilde", "at"],
        "name": "asciitilde_at.liga",
    },
    {  # ~>
        "chars": ["asciitilde", "greater"],
        "name": "asciitilde_greater.liga",
    },
    {  # ~-
        "chars": ["asciitilde", "hyphen"],
        "name": "asciitilde_hyphen.liga",
    },
    {  # *ptr
        "chars": ["asterisk"],
        "name": "asterisk.lc",
        "rule": " | [asterisk] @<{lookup}> | " + "[" + LOWERCASE + "]",
        "rule_kind": "coverage",
    },
    {  # **
        "chars": ["asterisk", "asterisk"],
        "name": "asterisk_asterisk.liga",
        "ignore_before": [
            "slash",  # /**
        ],
        "ignore_after": [
            "slash",  # **/
        ],
    },
    {  # ***
        "chars": ["asterisk", "asterisk", "asterisk"],
        "name": "asterisk_asterisk_asterisk.liga",
        "ignore_before": [
            "slash",  # /***
        ],
        "ignore_after": [
            "slash",  # ***/
        ],
    },
    {  # *>
        "chars": ["asterisk", "greater"],
        "name": "asterisk_greater.liga",
    },
    {  # */
        "chars": ["asterisk", "slash"],
        "name": "asterisk_slash.liga",
    },
    {  # \/   # new in 2.0
        "chars": ["backslash", "slash"],
        "name": "backslash_slash.liga",
    },
    {  # ||
        "chars": ["bar", "bar"],
        "name": "bar_bar.liga",
    },
    {  # |||  # absent from 2.0
        "chars": ["bar", "bar", "bar"],
        "name": "bar_bar_bar.liga",
    },
    {  # |||>
        "chars": ["bar", "bar", "bar", "greater"],
        "name": "bar_bar_bar_greater.liga",
    },
    {  # ||=  # FiraCode 6 only joins ||== and longer, so built from its pieces
        "chars": ["bar", "bar", "equal"],
        "name": "bar_bar_equal.liga",
        "parts": [None, "bar_bar_equal_start.seq", "equal_end.seq"],
    },
    {  # ||>
        "chars": ["bar", "bar", "greater"],
        "name": "bar_bar_greater.liga",
        "ignore_before": [
            "less",  # <||>
        ],
    },
    {  # ||-  # new in 2.0
        "chars": ["bar", "bar", "hyphen"],
        "name": "bar_bar_hyphen.liga",
        "parts": [None, "bar_bar_hyphen_start.seq", "hyphen_end.seq"],
    },
    {  # |}
        "chars": ["bar", "braceright"],
        "name": "bar_braceright.liga",
        "ignore_before": [
            "braceleft",  # {|}
        ],
    },
    {  # |]
        "chars": ["bar", "bracketright"],
        "name": "bar_bracketright.liga",
        "ignore_before": [
            "bracketleft",  # [|]
        ],
    },
    {  # |=  # FiraCode 6 only joins |== and longer, so built from its pieces
        "chars": ["bar", "equal"],
        "name": "bar_equal.liga",
        "parts": ["bar_equal_start.seq", "equal_end.seq"],
        "ignore_after": [
            "bar",  # |=|
        ],
    },
    {  # |=>  # new in 2.0
        "chars": ["bar", "equal", "greater"],
        "name": "bar_equal_greater.liga",
        "parts": ["bar_equal_start.seq", "equal_middle.seq", "greater_equal_end.seq"],
    },
    {  # |>
        "chars": ["bar", "greater"],
        "name": "bar_greater.liga",
    },
    {  # |-
        "chars": ["bar", "hyphen"],
        "name": "bar_hyphen.liga",
        "parts": ["bar_hyphen_start.seq", "hyphen_end.seq"],
        "ignore_after": [
            "bar",  # |-|
        ],
    },
    {  # |->  # new in 2.0
        "chars": ["bar", "hyphen", "greater"],
        "name": "bar_hyphen_greater.liga",
        "parts": [
            "bar_hyphen_start.seq",
            "hyphen_middle.seq",
            "greater_hyphen_end.seq",
        ],
    },
    {  # {|
        "chars": ["braceleft", "bar"],
        "name": "braceleft_bar.liga",
        "ignore_after": [
            "braceright",  # {|}
        ],
    },
    {  # [|
        "chars": ["bracketleft", "bar"],
        "name": "bracketleft_bar.liga",
        "ignore_after": [
            "bracketright",  # [|]
        ],
    },
    {  # ]#
        "chars": ["bracketright", "numbersign"],
        "name": "bracketright_numbersign.liga",
    },
    {  # X:
        "chars": ["colon"],
        "name": "colon.uc",
        "rule": "[" + TALL + "]" + " | [colon] @<{lookup}> | ",
        "rule_kind": "coverage",
    },
    {  # ::
        "chars": ["colon", "colon"],
        "name": "colon_colon.liga",
    },
    {  # :::
        "chars": ["colon", "colon", "colon"],
        "name": "colon_colon_colon.liga",
    },
    {  # ::=
        "chars": ["colon", "colon", "equal"],
        "name": "colon_colon_equal.liga",
    },
    {  # :=
        "chars": ["colon", "equal"],
        "name": "colon_equal.liga",
    },
    {  # :>  # FiraCode 6 only centers it vertically
        "chars": ["colon", "greater"],
        "name": "colon_greater.liga",
        "parts": ["colon.center", "greater.center"],
        "ignore_after": [
            "equal",  # :>=
            "colon",  # :>:
        ],
        "ignore_before": [
            "greater",  # >:>
        ],
    },
    {  # :<  # FiraCode 6 only centers it vertically
        "chars": ["colon", "less"],
        "name": "colon_less.liga",
        "parts": ["colon.center", "less.center"],
        "ignore_before": [
            "less",  # <:<
        ],
        "ignore_after": [
            "color",  # :<:
        ],
    },
    {  # $>
        "chars": ["dollar", "greater"],
        "name": "dollar_greater.liga",
    },
    {  # =~  # absent from 2.0, readd in 3.0
        "chars": ["equal", "asciitilde"],
        "name": "equal_asciitilde.ss07",
    },
    {  # =:=
        "chars": ["equal", "colon", "equal"],
        "name": "equal_colon_equal.liga",
        "parts": ["equal_start.seq", "colon_equal_middle.seq", "equal_end.seq"],
    },
    {  # ==
        "chars": ["equal", "equal"],
        "name": "equal_equal.liga",
        "ignore_before": [
            "bracketleft",  # [==
        ],
    },
    {  # ===
        "chars": ["equal", "equal", "equal"],
        "name": "equal_equal_equal.liga",
        "ignore_before": [
            "bracketleft",  # [===
        ],
    },
    {  # ==>
        "chars": ["equal", "equal", "greater"],
        "name": "equal_equal_greater.liga",
        "parts": ["equal_start.seq", "equal_middle.seq", "greater_equal_end.seq"],
        "ignore_before": [
            "bracketleft",  # [==>
        ],
    },
    {  # =!=
        "chars": ["equal", "exclam", "equal"],
        "name": "equal_exclam_equal.liga",
        "parts": ["equal_start.seq", "exclam_equal_middle.seq", "equal_end.seq"],
    },
    {  # =>
        "chars": ["equal", "greater"],
        "name": "equal_greater.liga",
        "parts": ["equal_start.seq", "greater_equal_end.seq"],
        "ignore_before": [
            "bracketleft",  # [=>
        ],
        "ignore_after": [
            "equal",  # =>=
        ],
    },
    {  # =>>
        "chars": ["equal", "greater", "greater"],
        "name": "equal_greater_greater.liga",
        "parts": ["equal_start.seq", None, "greater_greater_equal_end.seq"],
    },
    {  # =<<
        "chars": ["equal", "less", "less"],
        "name": "equal_less_less.liga",
        "parts": ["equal_start.seq", None, "less_less_equal_end.seq"],
    },
    {  # =/=
        "chars": ["equal", "slash", "equal"],
        "name": "equal_slash_equal.liga",
        "parts": ["equal_start.seq", "slash_equal_middle.seq", "equal_end.seq"],
    },
    {  # !~  # new in 3.0
        "chars": ["exclam", "asciitilde"],
        "name": "exclam_asciitilde.ss07",
    },
    {  # !=
        "chars": ["exclam", "equal"],
        "name": "exclam_equal.liga",
    },
    {  # !==
        "chars": ["exclam", "equal", "equal"],
        "name": "exclam_equal_equal.liga",
    },
    {  # !!
        "chars": ["exclam", "exclam"],
        "name": "exclam_exclam.liga",
    },
    {  # !!.
        "chars": ["exclam", "exclam", "period"],
        "name": "exclam_exclam_period.liga",
    },
    {  # >=
        "chars": ["greater", "equal"],
        "name": "greater_equal.liga",
        "ignore_after": [
            "less",  # >=<
        ],
        "ignore_before": [
            "equal",  # =>=
            "colon",  # :>=
        ],
    },
    {  # >:  # FiraCode 6 only centers it vertically
        "chars": ["greater", "colon"],
        "name": "greater_colon.liga",
        "parts": ["greater.center", "colon.center"],
        "ignore_after": [
            "greater",  # >:>
        ],
        "ignore_before": [
            "color",  # :>:
        ],
    },
    {  # >=>
        "chars": ["greater", "equal", "greater"],
        "name": "greater_equal_greater.liga",
        "parts": [
            "greater_equal_start.seq",
            "equal_middle.seq",
            "greater_equal_end.seq",
        ],
    },
    {  # >>
        "chars": ["greater", "greater"],
        "name": "greater_greater.liga",
        "ignore_before": [
            "asterisk",  # *>>
            "plus",  # +>>
            "dollar",  # $>>
        ],
    },
    {  # >>=  # FiraCode 6 only joins >>== and longer, so built from its pieces
        "chars": ["greater", "greater", "equal"],
        "name": "greater_greater_equal.liga",
        "parts": [None, "greater_greater_equal_start.seq", "equal_end.seq"],
        "ignore_before": [
            "equal",  # =>>=
        ],
        "ignore_after": [
            "greater",  # >>=>
        ],
    },
    {  # >>>
        "chars": ["greater", "greater", "greater"],
        "name": "greater_greater_greater.liga",
        "ignore_before": [
            "asterisk",  # *>>>
            "plus",  # +>>>
            "dollar",  # $>>>
        ],
    },
    {  # >>-
        "chars": ["greater", "greater", "hyphen"],
        "name": "greater_greater_hyphen.liga",
        "parts": [None, "greater_greater_hyphen_start.seq", "hyphen_end.seq"],
    },
    {  # >-
        "chars": ["greater", "hyphen"],
        "name": "greater_hyphen.liga",
        "parts": ["greater_hyphen_start.seq", "hyphen_end.seq"],
        "ignore_after": [
            "less",  # >-<
        ],
    },
    {  # >->
        "chars": ["greater", "hyphen", "greater"],
        "name": "greater_hyphen_greater.liga",
        "parts": [
            "greater_hyphen_start.seq",
            "hyphen_middle.seq",
            "greater_hyphen_end.seq",
        ],
    },
    {  # m-x, different with M-x
        "chars": ["hyphen"],
        "name": "hyphen.lc",
        "rule": "["
        + LOWERCASE
        + "]"
        + " | [hyphen] @<{lookup}> | "
        + "["
        + LOWERCASE
        + "]",
        "rule_kind": "coverage",
    },
    {  # -~
        "chars": ["hyphen", "asciitilde"],
        "name": "hyphen_asciitilde.liga",
    },
    {  # -|
        "chars": ["hyphen", "bar"],
        "name": "hyphen_bar.liga",
        "parts": ["hyphen_start.seq", "bar_hyphen_end.seq"],
        "ignore_before": [
            "bar",  # |-|
        ],
    },
    {  # ->
        "chars": ["hyphen", "greater"],
        "name": "hyphen_greater.liga",
        "parts": ["hyphen_start.seq", "greater_hyphen_end.seq"],
        "ignore_before": [
            "bracketleft",  # [->
        ],
    },
    {  # ->>
        "chars": ["hyphen", "greater", "greater"],
        "name": "hyphen_greater_greater.liga",
        "parts": ["hyphen_start.seq", None, "greater_greater_hyphen_end.seq"],
    },
    {  # --
        "chars": ["hyphen", "hyphen"],
        "name": "hyphen_hyphen.liga",
        "ignore_before": [
            "bracketleft",  # [--
        ],
    },
    {  # -->
        "chars": ["hyphen", "hyphen", "greater"],
        "name": "hyphen_hyphen_greater.liga",
        "parts": ["hyphen_start.seq", "hyphen_middle.seq", "greater_hyphen_end.seq"],
        "ignore_before": [
            "bracketleft",  # [-->
        ],
    },
    {  # ---
        "chars": ["hyphen", "hyphen", "hyphen"],
        "name": "hyphen_hyphen_hyphen.liga",
        "parts": ["hyphen_start.seq", "hyphen_middle.seq", "hyphen_end.seq"],
        "ignore_before": [
            "bracketleft",  # [---
        ],
    },
    {  # -<
        "chars": ["hyphen", "less"],
        "name": "hyphen_less.liga",
        "parts": ["hyphen_start.seq", "less_hyphen_end.seq"],
        "ignore_before": [
            "greater",  # >-<
        ],
    },
    {  # -<<
        "chars": ["hyphen", "less", "less"],
        "name": "hyphen_less_less.liga",
        "parts": ["hyphen_start.seq", None, "less_less_hyphen_end.seq"],
    },
    {  # <~
        "chars": ["less", "asciitilde"],
        "name": "less_asciitilde.liga",
    },
    {  # <~~
        "chars": ["less", "asciitilde", "asciitilde"],
        "name": "less_asciitilde_asciitilde.liga",
    },
    {  # <~>
        "chars": ["less", "asciitilde", "greater"],
        "name": "less_asciitilde_greater.liga",
    },
    {  # <*
        "chars": ["less", "asterisk"],
        "name": "less_asterisk.liga",
    },
    {  # <*>
        "chars": ["less", "asterisk", "greater"],
        "name": "less_asterisk_greater.liga",
    },
    {  # <|
        "chars": ["less", "bar"],
        "name": "less_bar.liga",
    },
    {  # <||
        "chars": ["less", "bar", "bar"],
        "name": "less_bar_bar.liga",
        "ignore_after": [
            "greater",  # <||>
        ],
    },
    {  # <|||
        "chars": ["less", "bar", "bar", "bar"],
        "name": "less_bar_bar_bar.liga",
    },
    {  # <|>
        "chars": ["less", "bar", "greater"],
        "name": "less_bar_greater.liga",
    },
    {  # <:  # FiraCode 6 only centers it vertically
        "chars": ["less", "colon"],
        "name": "less_colon.liga",
        "parts": ["less.center", "colon.center"],
        "ignore_after": [
            "less",  # <:<
        ],
        "ignore_before": [
            "color",  # :<:
        ],
    },
    {  # <$
        "chars": ["less", "dollar"],
        "name": "less_dollar.liga",
    },
    {  # <$>
        "chars": ["less", "dollar", "greater"],
        "name": "less_dollar_greater.liga",
    },
    {  # <=
        "chars": ["less", "equal"],
        "name": "less_equal.liga",
        "ignore_before": [
            "equal",  # =<=
        ],
    },
    {  # <=|  # new in 2.0
        "chars": ["less", "equal", "bar"],
        "name": "less_equal_bar.liga",
        "parts": ["less_equal_start.seq", "equal_middle.seq", "bar_equal_end.seq"],
    },
    {  # <==
        "chars": ["less", "equal", "equal"],
        "name": "less_equal_equal.liga",
        "parts": ["less_equal_start.seq", "equal_middle.seq", "equal_end.seq"],
    },
    {  # <==>
        "chars": ["less", "equal", "equal", "greater"],
        "name": "less_equal_equal_greater.liga",
        "parts": [
            "less_equal_start.seq",
            "equal_middle.seq",
            "equal_middle.seq",
            "greater_equal_end.seq",
        ],
    },
    {  # <=>
        "chars": ["less", "equal", "greater"],
        "name": "less_equal_greater.liga",
        "parts": ["less_equal_start.seq", "equal_middle.seq", "greater_equal_end.seq"],
    },
    {  # <=<
        "chars": ["less", "equal", "less"],
        "name": "less_equal_less.liga",
        "parts": ["less_equal_start.seq", "equal_middle.seq", "less_equal_end.seq"],
    },
    {  # <!--
        "chars": ["less", "exclam", "hyphen", "hyphen"],
        "name": "less_exclam_hyphen_hyphen.liga",
    },
    {  # <>
        "chars": ["less", "greater"],
        "name": "less_greater.liga",
    },
    {  # <-
        "chars": ["less", "hyphen"],
        "name": "less_hyphen.liga",
        "parts": ["less_hyphen_start.seq", "hyphen_end.seq"],
    },
    {  # <-|  # new in 2.0
        "chars": ["less", "hyphen", "bar"],
        "name": "less_hyphen_bar.liga",
        "parts": ["less_hyphen_start.seq", "hyphen_middle.seq", "bar_hyphen_end.seq"],
    },
    {  # <->
        "chars": ["less", "hyphen", "greater"],
        "name": "less_hyphen_greater.liga",
        "parts": [
            "less_hyphen_start.seq",
            "hyphen_middle.seq",
            "greater_hyphen_end.seq",
        ],
    },
    {  # <--
        "chars": ["less", "hyphen", "hyphen"],
        "name": "less_hyphen_hyphen.liga",
        "parts": ["less_hyphen_start.seq", "hyphen_middle.seq", "hyphen_end.seq"],
    },
    {  # <-<
        "chars": ["less", "hyphen", "less"],
        "name": "less_hyphen_less.liga",
        "parts": ["less_hyphen_start.seq", "hyphen_middle.seq", "less_hyphen_end.seq"],
    },
    {  # <<
        "chars": ["less", "less"],
        "name": "less_less.liga",
        "ignore_before": [
            "asterisk",  # *<<
            "plus",  # +<<
            "dollar",  # $<<
        ],
    },
    {  # <<=  # FiraCode 6 only joins <<== and longer, so built from its pieces
        "chars": ["less", "less", "equal"],
        "name": "less_less_equal.liga",
        "parts": [None, "less_less_equal_start.seq", "equal_end.seq"],
    },
    {  # <<-
        "chars": ["less", "less", "hyphen"],
        "name": "less_less_hyphen.liga",
        "parts": [None, "less_less_hyphen_start.seq", "hyphen_end.seq"],
    },
    {  # <<->> # new in 3.0
        "chars": ["less", "less", "hyphen", "greater", "greater"],
        "name": "less_less_hyphen_greater_greater.liga",
        "parts": [
            None,
            "less_less_hyphen_start.seq",
            "hyphen_middle.seq",
            None,
            "greater_greater_hyphen_end.seq",
        ],
    },
    {  # <<<
        "chars": ["less", "less", "less"],
        "name": "less_less_less.liga",
        "ignore_before": [
            "asterisk",  # *<<<
            "plus",  # +<<<
            "dollar",  # $<<<
        ],
    },
    {  # <+
        "chars": ["less", "plus"],
        "name": "less_plus.liga",
    },
    {  # <+>
        "chars": ["less", "plus", "greater"],
        "name": "less_plus_greater.liga",
    },
    {  # </
        "chars": ["less", "slash"],
        "name": "less_slash.liga",
    },
    {  # </>
        "chars": ["less", "slash", "greater"],
        "name": "less_slash_greater.liga",
    },
    {  # #{
        "chars": ["numbersign", "braceleft"],
        "name": "numbersign_braceleft.liga",
        "ignore_after": [
            "braceright",  # #{}
        ],
    },
    {  # #[
        "chars": ["numbersign", "bracketleft"],
        "name": "numbersign_bracketleft.liga",
    },
    {  # #:
        "chars": ["numbersign", "colon"],
        "name": "numbersign_colon.liga",
    },
    {  # #=
        "chars": ["numbersign", "equal"],
        "name": "numbersign_equal.liga",
    },
    {  # #!
        "chars": ["numbersign", "exclam"],
        "name": "numbersign_exclam.liga",
    },
    {  # ##
        "chars": ["numbersign", "numbersign"],
        "name": "numbersign_numbersign.liga",
        "parts": ["numbersign_start.seq", "numbersign_end.seq"],
    },
    {  # ###
        "chars": ["numbersign", "numbersign", "numbersign"],
        "name": "numbersign_numbersign_numbersign.liga",
        "parts": [
            "numbersign_start.seq",
            "numbersign_middle.seq",
            "numbersign_end.seq",
        ],
    },
    {  # ####
        "chars": ["numbersign", "numbersign", "numbersign", "numbersign"],
        "name": "numbersign_numbersign_numbersign_numbersign.liga",
        "parts": [
            "numbersign_start.seq",
            "numbersign_middle.seq",
            "numbersign_middle.seq",
            "numbersign_end.seq",
        ],
    },
    {  # #(
        "chars": ["numbersign", "parenleft"],
        "name": "numbersign_parenleft.liga",
    },
    {  # #?
        "chars": ["numbersign", "question"],
        "name": "numbersign_question.liga",
    },
    {  # #_
        "chars": ["numbersign", "underscore"],
        "name": "numbersign_underscore.liga",
    },
    {  # #_(
        "chars": ["numbersign", "underscore", "parenleft"],
        "name": "numbersign_underscore_parenleft.liga",
    },
    {  # %%
        "chars": ["percent", "percent"],
        "name": "percent_percent.liga",
    },
    {  # .=  # optional (cv32) since FiraCode 6.0
        "chars": ["period", "equal"],
        "name": "period_equal.cv32",
    },
    {  # .-  # optional (cv25) since FiraCode 6.0
        "chars": ["period", "hyphen"],
        "name": "period_hyphen.cv25",
    },
    {  # ..
        "chars": ["period", "period"],
        "name": "period_period.liga",
    },
    {  # ..=  # absent from 2.0, readd in 3.0
        "chars": ["period", "period", "equal"],
        "name": "period_period_equal.liga",
    },
    {  # ..<
        "chars": ["period", "period", "less"],
        "name": "period_period_less.liga",
    },
    {  # ...
        "chars": ["period", "period", "period"],
        "name": "period_period_period.liga",
    },
    {  # .?
        "chars": ["period", "question"],
        "name": "period_question.liga",
    },
    {  # m+x, different with M+x
        "chars": ["plus"],
        "name": "plus.lc",
        "rule": "["
        + LOWERCASE
        + "]"
        + " | [plus] @<{lookup}> | "
        + "["
        + LOWERCASE
        + "]",
        "rule_kind": "coverage",
    },
    {  # +>
        "chars": ["plus", "greater"],
        "name": "plus_greater.liga",
    },
    {  # ++
        "chars": ["plus", "plus"],
        "name": "plus_plus.liga",
    },
    {  # +++
        "chars": ["plus", "plus", "plus"],
        "name": "plus_plus_plus.liga",
    },
    {  # ?=
        "chars": ["question", "equal"],
        "name": "question_equal.liga",
    },
    {  # ?.
        "chars": ["question", "period"],
        "name": "question_period.liga",
    },
    {  # ??
        "chars": ["question", "question"],
        "name": "question_question.liga",
    },
    {  # ;;
        "chars": ["semicolon", "semicolon"],
        "name": "semicolon_semicolon.liga",
    },
    {  # /*
        "chars": ["slash", "asterisk"],
        "name": "slash_asterisk.liga",
    },
    {  # /\   # new in 2.0
        "chars": ["slash", "backslash"],
        "name": "slash_backslash.liga",
    },
    {  # /=
        "chars": ["slash", "equal"],
        "name": "slash_equal.liga",
        "parts": ["slash_equal_start.seq", "equal_end.seq"],
    },
    {  # /==
        "chars": ["slash", "equal", "equal"],
        "name": "slash_equal_equal.liga",
        "parts": ["slash_equal_start.seq", "equal_middle.seq", "equal_end.seq"],
    },
    {  # />
        "chars": ["slash", "greater"],
        "name": "slash_greater.liga",
    },
    {  # //
        "chars": ["slash", "slash"],
        "name": "slash_slash.liga",
    },
    {  # ///
        "chars": ["slash", "slash", "slash"],
        "name": "slash_slash_slash.liga",
    },
    {  # _|_
        "chars": ["underscore", "bar", "underscore"],
        "name": "underscore_bar_underscore.liga",
        "parts": [
            "underscore_start.seq",
            "bar_underscore_middle.seq",
            "underscore_end.seq",
        ],
    },
    {  # __
        "chars": ["underscore", "underscore"],
        "name": "underscore_underscore.liga",
        "parts": ["underscore_start.seq", "underscore_end.seq"],
    },
    {  # www
        "chars": ["w", "w", "w"],
        "name": "w_w_w.liga",
    },
    {  # 0xFF, 1920x1080
        "chars": ["x"],
        "name": "x.multiply",
        "rule": "[zero] | [x] @<{lookup}> | [" + HEX_DIGIT + "]",
        "rule_kind": "coverage",
    },
]
