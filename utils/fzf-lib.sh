#!/usr/bin/env bash
#
# fzf-lib.sh -- use fzf to open files from ~/library
#
# Usage: fzf-lib.sh [-c]
#
#   -c      Remake cache file
#
# Ignore solution PDFs, html files of course websites etc. by prepending the
# directories, files, with _
#

cache="${HOME}/.cache/fzf-lib.cache"
mtime=$(stat -c "%Y" "$cache" 2>/dev/null)
ctime=$(date "+%s")

if ! [[ -f "$cache" ]] || (( ctime - mtime > 43200 )) || [[ "$1" = "-c" ]]
then
    cd ~/library
    # Exclude everything from the zeal directory.
    find . -type f \( -iname '*.azw3' -o \
                      -iname '*.djvu' -o \
                      -iname '*.epub' -o \
                      -iname '*.htm'  -o \
                      -iname '*.html' -o \
                      -iname '*.lit'  -o \
                      -iname '*.maff' -o \
                      -iname '*.mobi' -o \
                      -iname '*.pdf'  -o \
                      -iname '*.ps'   -o \
                      -iname '*.txt' \) -not -path '*zeal/*' -not -path '*solutions/*' >"$cache"
    cd "$OLDPWD"
    echo >&2 "fzlib: cache updated."
fi

file=$(fzf -1 -0 <"$cache")
if [[ -n "$file" ]]
then
    nohup xdg-open "${HOME}/library/${file}" &>/dev/null &
    echo >&2 "${HOME}/library/${file}"
fi
