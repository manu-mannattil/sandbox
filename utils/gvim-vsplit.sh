#!/bin/sh
#
# gvim-vsplit -- open the file in a vertical split in a remote Vim window.
#
# I wrote this in a Reddit thread https://redd.it/4jucie
#
# 2016-05-18 20:27 IST
#


GVIM="/usr/bin/gvim"

# Use the most recent gVim server.
server=$("$GVIM" --serverlist | tail -n -1)

if test "$server"
then
    printf >&2 "Connecting to '${server}' ..."
    exec "$GVIM" --servername "$server"                                         \
                    --remote-send "<ESC>:vsplit <C-R>=fnameescape('${1}')<CR><CR>" \
                    >/dev/null </dev/null 2>&1
else
    printf >&2 "No existing Vim sessions."
    exec "$GVIM" "$@" >/dev/null </dev/null 2>&1
fi
