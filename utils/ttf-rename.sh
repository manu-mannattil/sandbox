#!/bin/sh
#
# ------------  --------------------------------------------------------
#         file  ttf-rename.sh
#  description  Change font name in TTF files.
#      created  2016-03-06 17:08 IST
#     modified  2016-03-06 17:08 IST
# ------------  --------------------------------------------------------
#
# Usage: ttf-rename <name> <file>.ttf
#
# I don't know much about font names (i.e., what's the difference
# between the family name, font name, variant, etc.).  This script will
# use ONE SINGLE NAME for all those things.
#
# I originally created this script to use arbitrary font files with
# matplotlib.  It seems that matplotlib picks fonts based on their
# family name alone.  So you might get "Helvetica Condensed Black" or
# something if you just ask for "Helvetica".
#

set -e

font_name_xml() {
  # Generates XML to be nested inside <name> </name>.
  # Template is based on Inconsolata's TTF file.
  cat <<EOF
    <namerecord nameID="0" platformID="1" platEncID="0" langID="0x0">
      ${1}
    </namerecord>
    <namerecord nameID="1" platformID="1" platEncID="0" langID="0x0">
      ${1}
    </namerecord>
    <namerecord nameID="2" platformID="1" platEncID="0" langID="0x0">
      Regular
    </namerecord>
    <namerecord nameID="3" platformID="1" platEncID="0" langID="0x0">
      ${1}; 1.0; $(date +%Y-%m-%d)
    </namerecord>
    <namerecord nameID="4" platformID="1" platEncID="0" langID="0x0">
      ${1}
    </namerecord>
    <namerecord nameID="5" platformID="1" platEncID="0" langID="0x0">
      Version 1.0
    </namerecord>
    <namerecord nameID="6" platformID="1" platEncID="0" langID="0x0">
      ${1}
    </namerecord>
    <namerecord nameID="0" platformID="3" platEncID="1" langID="0x409">
      ${1}
    </namerecord>
    <namerecord nameID="1" platformID="3" platEncID="1" langID="0x409">
      ${1}
    </namerecord>
    <namerecord nameID="2" platformID="3" platEncID="1" langID="0x409">
      Regular
    </namerecord>
    <namerecord nameID="3" platformID="3" platEncID="1" langID="0x409">
      ${1}; 1.0; $(date +%Y-%m-%d)
    </namerecord>
    <namerecord nameID="4" platformID="3" platEncID="1" langID="0x409">
      ${1}
    </namerecord>
    <namerecord nameID="5" platformID="3" platEncID="1" langID="0x409">
      Version 1.0
    </namerecord>
    <namerecord nameID="6" platformID="3" platEncID="1" langID="0x409">
      ${1}
    </namerecord>
EOF
}

tmpdir="$(mktemp -d)"
trap 'rm -rf "$tmpdir" >/dev/null 2>&1' EXIT
trap 'exit 2' HUP INT QUIT TERM

if [ $# -lt 2 ]; then
  echo >&2 "usage: ttf-rename.sh <name> <file>.ttf"
  exit 1
fi

font_name="$1"
font_file="$2"
font_ttx="${tmpdir}/orig.ttx"
font_ttx_edit="${tmpdir}/edit.ttx"

echo >&2 "Uncompressing TTF file..."
ttx -o "$font_ttx" "$font_file" >&2

echo >&2
echo >&2 "Renaming TTF file..."

{ sed -n -e '0,/ *<name>$/p' "$font_ttx"
  font_name_xml "$font_name"
  sed -n -e '/ *<\/name>$/,$p' "$font_ttx"
} >"$font_ttx_edit"

echo >&2
echo >&2 "Writing back to a TTF file.."
ttx -o "${font_name}.ttf" "$font_ttx_edit" >&2

echo >&2
echo >&2 "${font_file} -> ${font_name}.ttf"
