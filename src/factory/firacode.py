"""Specification of font ligatures from FiraCode"""

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
    {  # &&&  # absent from 2.0
        "chars": ["ampersand", "ampersand", "ampersand"],
        "name": "ampersand_ampersand_ampersand.liga",
    },
    {  # ^=
        "chars": ["asciicircum", "equal"],
        "name": "asciicircum_equal.liga",
    },
    {  # ~~
        "chars": ["asciitilde", "asciitilde"],
        "name": "asciitilde_asciitilde.liga",
    },
    {  # ~~~  # absent from 2.0
        "chars": ["asciitilde", "asciitilde", "asciitilde"],
        "name": "asciitilde_asciitilde_asciitilde.liga",
    },
    {  # ~~>
        "chars": ["asciitilde", "asciitilde", "greater"],
        "name": "asciitilde_asciitilde_greater.liga",
    },
    {  # ~@
        "chars": ["asciitilde", "at"],
        "name": "asciitilde_at.liga",
    },
    {  # ~=  # absent from 3.0
        "chars": ["asciitilde", "equal"],
        "name": "asciitilde_equal.liga",
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
    {  # **/  # absent from 2.0
        "chars": ["asterisk", "asterisk", "slash"],
        "name": "asterisk_asterisk_slash.liga",
    },
    {  # *>
        "chars": ["asterisk", "greater"],
        "name": "asterisk_greater.liga",
    },
    {  # */
        "chars": ["asterisk", "slash"],
        "name": "asterisk_slash.liga",
    },
    {  # \\   # absent from 2.0
        "chars": ["backslash", "backslash"],
        "name": "backslash_backslash.liga",
    },
    {  # \\\  # absent from 2.0
        "chars": ["backslash", "backslash", "backslash"],
        "name": "backslash_backslash_backslash.liga",
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
    {  # ||=
        "chars": ["bar", "bar", "equal"],
        "name": "bar_bar_equal.liga",
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
    {  # |=
        "chars": ["bar", "equal"],
        "name": "bar_equal.liga",
        "ignore_after": [
            "bar",  # |=|
        ],
    },
    {  # |=>  # new in 2.0
        "chars": ["bar", "equal", "greater"],
        "name": "bar_equal_greater.liga",
    },
    {  # |>
        "chars": ["bar", "greater"],
        "name": "bar_greater.liga",
    },
    {  # |-
        "chars": ["bar", "hyphen"],
        "name": "bar_hyphen.liga",
        "ignore_after": [
            "bar",  # |-|
        ],
    },
    {  # |->  # new in 2.0
        "chars": ["bar", "hyphen", "greater"],
        "name": "bar_hyphen_greater.liga",
    },
    {  # {|
        "chars": ["braceleft", "bar"],
        "name": "braceleft_bar.liga",
        "ignore_after": [
            "braceright",  # {|}
        ],
    },
    {  # {-  # absent from 2.0
        "chars": ["braceleft", "hyphen"],
        "name": "braceleft_hyphen.liga",
    },
    {  # [|
        "chars": ["bracketleft", "bar"],
        "name": "bracketleft_bar.liga",
        "ignore_after": [
            "bracketright",  # [|]
        ],
    },
    {  # []  # absent from 2.0
        "chars": ["bracketleft", "bracketright"],
        "name": "bracketleft_bracketright.liga",
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
    {  # :>
        "chars": ["colon", "greater"],
        "name": "colon_greater.liga",
        "ignore_after": [
            "equal",  # :>=
            "colon",  # :>:
        ],
        "ignore_before": [
            "greater",  # >:>
        ],
    },
    {  # :<
        "chars": ["colon", "less"],
        "name": "colon_less.liga",
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
        "ignore_before": [
            "bracketleft",  # [==>
        ],
    },
    {  # =!=
        "chars": ["equal", "exclam", "equal"],
        "name": "equal_exclam_equal.liga",
    },
    {  # =>
        "chars": ["equal", "greater"],
        "name": "equal_greater.liga",
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
    },
    {  # =<<
        "chars": ["equal", "less", "less"],
        "name": "equal_less_less.liga",
    },
    {  # =/=
        "chars": ["equal", "slash", "equal"],
        "name": "equal_slash_equal.liga",
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
    {  # !!!  # absent from 2.0
        "chars": ["exclam", "exclam", "exclam"],
        "name": "exclam_exclam_exclam.liga",
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
    {  # >:
        "chars": ["greater", "colon"],
        "name": "greater_colon.liga",
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
    {  # >>=
        "chars": ["greater", "greater", "equal"],
        "name": "greater_greater_equal.liga",
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
    },
    {  # >-
        "chars": ["greater", "hyphen"],
        "name": "greater_hyphen.liga",
        "ignore_after": [
            "less",  # >-<
        ],
    },
    {  # >->
        "chars": ["greater", "hyphen", "greater"],
        "name": "greater_hyphen_greater.liga",
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
        "ignore_before": [
            "bar",  # |-|
        ],
    },
    {  # -}  # absent from 2.0
        "chars": ["hyphen", "braceright"],
        "name": "hyphen_braceright.liga",
    },
    {  # ->
        "chars": ["hyphen", "greater"],
        "name": "hyphen_greater.liga",
        "ignore_before": [
            "bracketleft",  # [->
        ],
    },
    {  # ->>
        "chars": ["hyphen", "greater", "greater"],
        "name": "hyphen_greater_greater.liga",
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
        "ignore_before": [
            "bracketleft",  # [-->
        ],
    },
    {  # ---
        "chars": ["hyphen", "hyphen", "hyphen"],
        "name": "hyphen_hyphen_hyphen.liga",
        "ignore_before": [
            "bracketleft",  # [---
        ],
    },
    {  # -<
        "chars": ["hyphen", "less"],
        "name": "hyphen_less.liga",
        "ignore_before": [
            "greater",  # >-<
        ],
    },
    {  # -<<
        "chars": ["hyphen", "less", "less"],
        "name": "hyphen_less_less.liga",
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
    {  # <:
        "chars": ["less", "colon"],
        "name": "less_colon.liga",
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
    },
    {  # <==
        "chars": ["less", "equal", "equal"],
        "name": "less_equal_equal.liga",
    },
    {  # <==>
        "chars": ["less", "equal", "equal", "greater"],
        "name": "less_equal_equal_greater.liga",
    },
    {  # <=>
        "chars": ["less", "equal", "greater"],
        "name": "less_equal_greater.liga",
    },
    {  # <=<
        "chars": ["less", "equal", "less"],
        "name": "less_equal_less.liga",
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
    },
    {  # <-|  # new in 2.0
        "chars": ["less", "hyphen", "bar"],
        "name": "less_hyphen_bar.liga",
    },
    {  # <->
        "chars": ["less", "hyphen", "greater"],
        "name": "less_hyphen_greater.liga",
    },
    {  # <--
        "chars": ["less", "hyphen", "hyphen"],
        "name": "less_hyphen_hyphen.liga",
    },
    {  # <-<
        "chars": ["less", "hyphen", "less"],
        "name": "less_hyphen_less.liga",
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
    {  # <<=
        "chars": ["less", "less", "equal"],
        "name": "less_less_equal.liga",
    },
    {  # <<-
        "chars": ["less", "less", "hyphen"],
        "name": "less_less_hyphen.liga",
    },
    {  # <<->> # new in 3.0
        "chars": ["less", "less", "hyphen", "greater", "greater"],
        "name": "less_less_hyphen_greater_greater.liga",
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
    },
    {  # ###
        "chars": ["numbersign", "numbersign", "numbersign"],
        "name": "numbersign_numbersign_numbersign.liga",
    },
    {  # ####
        "chars": ["numbersign", "numbersign", "numbersign", "numbersign"],
        "name": "numbersign_numbersign_numbersign_numbersign.liga",
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
    {  # %%%  # absent from 2.0
        "chars": ["percent", "percent", "percent"],
        "name": "percent_percent_percent.liga",
    },
    {  # .=
        "chars": ["period", "equal"],
        "name": "period_equal.liga",
    },
    {  # .-
        "chars": ["period", "hyphen"],
        "name": "period_hyphen.liga",
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
    {  # ?:  # absent from 3.0
        "chars": ["question", "colon"],
        "name": "question_colon.liga",
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
    {  # ???  # absent from 2.0
        "chars": ["question", "question", "question"],
        "name": "question_question_question.liga",
    },
    {  # ;;
        "chars": ["semicolon", "semicolon"],
        "name": "semicolon_semicolon.liga",
    },
    {  # ;;;  # absent from 2.0
        "chars": ["semicolon", "semicolon", "semicolon"],
        "name": "semicolon_semicolon_semicolon.liga",
    },
    {  # /*
        "chars": ["slash", "asterisk"],
        "name": "slash_asterisk.liga",
    },
    {  # /**  # absent from 2.0
        "chars": ["slash", "asterisk", "asterisk"],
        "name": "slash_asterisk_asterisk.liga",
    },
    {  # /\   # new in 2.0
        "chars": ["slash", "backslash"],
        "name": "slash_backslash.liga",
    },
    {  # /=
        "chars": ["slash", "equal"],
        "name": "slash_equal.liga",
    },
    {  # /==
        "chars": ["slash", "equal", "equal"],
        "name": "slash_equal_equal.liga",
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
    },
    {  # __
        "chars": ["underscore", "underscore"],
        "name": "underscore_underscore.liga",
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
