#!/usr/bin/env bash
#
# dynamic-colors.sh -- psychedelic xterm
#
# BTW, this only works in *xterm*.  Someone got it working on iTerm too
# (see Reddit discussion).  But it'll be really nice if there was
# a terminal agnostic way to do this (or at least do it for the major
# terms - rxvt, aterm, uterm, st, etc.).
#
# Source: http://rcr.io/words/dynamic-xterm-colors.html Discussion:
# http://www.reddit.com/r/linux/comments/2ds0he/xterm_party/
#
# -m, 2014-08-30 00:00 IST
#

A=0;
F="0.1"

while true; do

[ $A == 628318 ] && A=0 || A=$((A + 1))

R=$(echo "s ($F*$A + 0)*127 + 128" | bc -l | cut -d'.' -f1)
B=$(echo "s ($F*$A + 2)*127 + 128" | bc -l | cut -d'.' -f1)
G=$(echo "s ($F*$A + 4)*127 + 128" | bc -l | cut -d'.' -f1)

printf "\033]10;#%02x%02x%02x\007" $R $B $G

sleep 0.01
done
