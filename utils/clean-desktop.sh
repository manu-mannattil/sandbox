#!/usr/bin/env bash
#
# clean-desktop.sh -- clean temporary/cache files in a GNU/Linux desktop
#
# This script removes *all* top-level hidden files and
# directories in $HOME apart from a few.
#
# NOTE: Please do NOT use this script without going through it first and
# noting what files will be kept.
#
# Requires: GNU coreutils.
#

echo "\
This script will PERMANENTLY remove cache files and other 'temporary'
files, which may affect the performance of your system."

read -r -p "-> Type OKAY to continue: "
[[ $REPLY == "OKAY" ]] || {
    echo "Aborted."
    exit 1
}

set -euo pipefail

pushd "$HOME"

cache="$HOME/clean-desktop-$(date +%Y%m%d%H%M%S)"
mkdir -p "$cache"

cache() {
    for arg
    do
        if ! [[ -e "$arg" || -d "$arg" || -h "$arg" ]]
        then
            echo "Cannot cache '$arg' as it does not exit (or is not readable)."
            read -r -p "-> Type OKAY to continue: "
            if [[ $REPLY == "OKAY" ]]
            then
                continue
            else
                echo "Aborted."
                popd
                exit 1
            fi
        fi

        echo "Caching: '$arg'"
        cp --archive --link --no-clobber --parents -- "$arg" "$cache"
    done
}

_rm() {
    rm --one-file-system -rf "$@"
}

# Pre-caching commands -------------------------------------------------

# Mozilla Firefox
if [[ -f "$HOME/.config/mozilla/firefox/profiles.ini" ]]
then
    while IFS= read -r profile
    do
        _rm "$HOME/.cache/mozilla/firefox/$profile"                         \
            "$HOME/.config/mozilla/firefox/$profile/content-prefs.sqlite"   \
            "$HOME/.config/mozilla/firefox/$profile/cookies.sqlite"         \
            "$HOME/.config/mozilla/firefox/$profile/formhistory.sqlite"     \
            "$HOME/.config/mozilla/firefox/$profile/storage.sqlite"         \
            "$HOME/.config/mozilla/firefox/$profile/webappsstore.sqlite"    \
            "$HOME/.config/mozilla/firefox/$profile/crashes"                \
            "$HOME/.config/mozilla/firefox/$profile/datareporting"          \
            "$HOME/.config/mozilla/firefox/$profile/minidumps"              \
            "$HOME/.config/mozilla/firefox/$profile/storage"
    done < <(sed -n 's/^Path=//p' "$HOME/.config/mozilla/firefox/profiles.ini")
fi

# vcpkg
_rm ~/.local/vcpkg/buildtrees/*
_rm ~/.local/vcpkg/downloads/*

# torrents
_rm ~/*.torrent
_rm ~/downloads/*.torrent

# python/mamba
mamba clean --all
_rm ~/.local/miniforge/var/cache/*
_rm ~/.local/share/pipx/logs/*

# Caching --------------------------------------------------------------

cache ".bashrc_local"

cache ".config/mozilla"
cache ".thunderbird"

cache ".ssh/id_"*
cache ".ssh/known_hosts"

cache ".gnupg/private-keys-v1.d"
cache ".gnupg/pubring.kbx"
cache ".gnupg/trustdb.gpg"

cache ".cache/restic"

cache ".cache/maestral"
cache ".config/maestral"
cache ".local/share/maestral"

cache ".local/miniforge"
cache ".local/pipx-bin"
cache ".local/share/pipx"
cache ".local/venvs"

cache ".local/vcpkg"

cache ".config/syncthing"
cache ".local/state/syncthing"
cache ".local/share/syncthing"

cache ".Mathematica/Licensing"

cache ".config/Ferdium"

cache ".config/Signal"

cache ".config/systemd"

cache ".texmf"

cache ".config/libreoffice/4/user/template"

cache ".config/obsidian"

# How many files does Zoom need?  Uggh.
cache ".zoom"
cache ".config/zoom.conf"
cache ".config/zoomus.conf"
cache ".config/Unknown Organization/zoom.conf"

cache ".wine"
cache ".mp3tag.d"

# Clean and restore ----------------------------------------------------

echo "Removing all top-level hidden files from '$HOME'"
_rm .*

echo "Restoring files from '$cache'"
cp --archive --link "$cache"/. ~

# Post cleanup ---------------------------------------------------------

mkdir -p ".cache"

echo "Running post cleanup actions"
[[ -d ~/music/.lyrics ]] && ln -s ~/music/.lyrics ~/.cache/lyrics

printf "\n" >| "${HISTFILE:-${HOME}/.bash_history}"

popd
