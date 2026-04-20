#!/bin/sh
#
# -----------  -----------------------------------------------------------
#        file  cutvid.sh
# description  Cut part of video using FFMpeg
#     created  2014-02-28 XX:XX IST
#    modified  2014-12-30 23:51 IST
# -----------  -----------------------------------------------------------
#

die() {
    echo >&2 "$1"
    echo >&2 "usage: cutvid -s <start> [-e <end>] -i <input> -o <output>"
    exit 1
}

while getopts ":s:e:i:o:" opt; do
    case "$opt" in
        s)  start="$OPTARG"                                 ;;
        e)  end="$OPTARG"                                   ;;
        i)  input="$OPTARG"                                 ;;
        o)  output="$OPTARG"                                ;;
        :)  die "cutvid: -${OPTARG} requires an argument"   ;;
        \?) die "cutvid: -${OPTARG} is not an valid option" ;;
    esac
done

[ -n "$start" ]  || die "cutvid: starting time needs to be specified"
[ -n "$input" ]  || die "cutvid: input file needs to be specified"
[ -n "$output" ] || die "cutvid: output file needs to be specified"

if [ -n "$end" ]; then
    ffmpeg -i "$input"  \
           -ss "$start" \
           -to "$end"   \
           -acodec copy \
           -vcodec copy \
           -async 1     \
           "$output"
else
    ffmpeg -i "$input"  \
           -ss "$start" \
           -acodec copy \
           -vcodec copy \
           -async 1     \
           "$output"
fi
