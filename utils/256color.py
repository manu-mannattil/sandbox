#!/usr/bin/env python
#
# 256color.py -- print 256 ASCII colors and their hex equivalent.
#
# This script prints a chart of 256 ASCII colors and their hex
# equivalents.  This is especially useful when designing Vim
# colorschemes.  Adapted from [1].
#
# [1]: https://gist.github.com/justinabrahms/1047767
#
# -m, 2017-04-28 20:36 IST
#

from __future__ import print_function
import sys

print("Color indexes should be drawn in bold text of the same color.")
print()

colored = [0] + [0x5f + 40 * n for n in range(0, 5)]
colored_palette = [
    "#%02x%02x%02x" % (r, g, b)
    for r in colored
    for g in colored
    for b in colored
]

grayscale = [0x08 + 10 * n for n in range(0, 24)]
grayscale_palette = [
    "#%02x%02x%02x" % (a, a, a)
    for a in grayscale
]

normal = "\033[38;5;%sm"
bold = "\033[1;38;5;%sm"
reset = "\033[0m"

for (i, color) in enumerate(colored_palette + grayscale_palette, 16):
    index = (bold + "%4s" + reset) % (i, str(i) + ':')
    hex   = (normal + "%s" + reset) % (i, color)
    newline = '\n' if i % 6 == 3 else ''
    sys.stdout.write('{}{}{} '.format(index, hex, newline))
