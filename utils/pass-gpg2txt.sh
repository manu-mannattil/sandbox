#!/usr/bin/env bash
#
# pass-gpg2txt.sh -- convert all *.gpg files in a pass store to plain text
#
# Warning: It's very unsafe to use this script.
#

[[ $# -lt 3 ]] || {
   echo >&2 "usage: ${0##*/} <store> <dir>"
}

cp -r "$1" "$2"

pushd "$2"

while IFS= read -r gpg
do
    txt="${gpg%.*}.txt"
    gpg -q --decrypt "$gpg" >"$txt"
    echo >&2 "${0##*/}: $gpg -> $txt"
done < <(find -type f -name '*.gpg')

popd
