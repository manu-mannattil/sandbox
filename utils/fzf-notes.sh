#!/usr/bin/env bash
#
# fzf-notes.sh -- use fzf to open files from ~/documents/notes
#
# Usage: fzf-notes.sh [-c]
#
#   -c      Remake cache file
#
# Ignore solution PDFs, html files of course websites etc. by prepending the
# directories, files, with _
#

cache="${HOME}/.cache/fzf-notes.cache"
mtime=$(stat -c "%Y" "$cache" 2>/dev/null)
ctime=$(date "+%s")

if ! [[ -f "$cache" ]] || (( ctime - mtime > 43200 )) || [[ "$1" = "-c" ]]
then
    pushd ~/documents/notes
    # Exclude everything from the zeal directory.
    find . -type f \( -iname '*.tex'    -o  \
                      -iname '*.pdf'    -o  \
                      -iname '*.md'     -o  \
                      -iname '*.txt' \) -not -path '*figures/*' >"$cache"
    popd
    echo >&2 "fzf-notes: cache updated."
fi

file=$(fzf -1 -0 <"$cache")
if [[ -n "$file" ]]
then
    nohup xdg-open "$HOME/documents/notes/$file" &>/dev/null &
    echo >&2 "$HOME/documents/notes/$file"
fi
