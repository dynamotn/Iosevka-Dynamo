#!/usr/bin/env python3
"""Show statistic of font"""

import fontforge
import sys

input_font_path = sys.argv[1]
font = fontforge.open(input_font_path)

for field in dir(font):
    if field.startswith("__"):
        continue
    value = getattr(font, field)
    if "built-in" in str(value):
        continue
    print("%s = %s" % (field, value))
