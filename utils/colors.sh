#!/bin/sh
#
# ------------  ---------------------------------------------------------
#         file  colors
#  description  Print tables of terminal colors
#      created  2012-XX-XX XX:XX IST
#     modified  2015-11-21 21:47 IST
# ------------  ---------------------------------------------------------
#
# Must rewrite properly in some other language -- Python perhaps.  It must
# include options to generate a 256 color cube, 256 color rows, etc.
#

text="  gYw  "
clrfg="\033[38;5;"
clrbg="\033[48;5;"
reset="\033[0m"

header() {
  echo
  for i in $(seq $1 $2); do
    printf "%8d" $i
  done
  echo
}

table() {
  for i in $(seq $1 $2); do
    printf "%3d" $i
    for j in $(seq $3 $4); do
      printf " ${clrbg}${i}m${clrfg}${j}m${text}${reset}"
    done
    echo
  done
}

# print all the tables
header 0  7; table 0  7 0  7
header 0  7; table 8 15 0  7
header 8 15; table 0  7 8 15
header 8 15; table 8 15 8 15
