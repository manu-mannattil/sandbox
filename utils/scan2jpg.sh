#!/bin/sh
#
# ------------  --------------------------------------------------------
#         file  scan2jpg.sh
#  description  Scan document and convert to JPEG
# dependencies  convert (ImageMagick), mktemp, scaimage
#      created  2015-02-2X XX:XX IST
#     modified  2016-10-21 06:41 IST
# ------------  --------------------------------------------------------
#
#: usage: scan2jpg.sh [-d <dpi>] [<output>]
#:
#: If no output file is specified, scan2jpg.sh will put a
#: compressed .jpg file of 600 DPI resolution in the current
#: directory.
#

tmpfile="$(mktemp -t scan.XXXXXX.tiff)"
trap 'rm -rf "$tmpfile" >/dev/null 2>&1' EXIT
trap 'exit 2' HUP INT QUIT TERM

dpi=600

while getopts ":hvd:" opt
do
    case "$opt" in
        h)  grep '^#:' <"$0" | cut >&2 -c 4-
            exit 0 ;;
        v)  set -x ;;
        d)  dpi="$OPTARG" ;;
        :)  printf >&2 "%s: -%s requires an argument\n" "${0##*/}" "$OPTARG"
            exit 1 ;;
        \?) printf >&2 "%s: -%s is not a valid option\n" "${0##*/}" "$OPTARG"
            exit 1 ;;
    esac
done
shift $(( OPTIND - 1 ))

scanimage --mode=Color --progress --format=tiff --resolution "$dpi" >"$tmpfile" || exit 1

if test "$1"
then
    convert -strip "$tmpfile" "$1"
else
    output=$(date +"scan-%Y%m%dT%H%M%S%Z.jpg")
    # http://stackoverflow.com/a/7262050
    convert -strip -interlace Plane -quality 85% "$tmpfile" "${PWD}/${output}"
fi
