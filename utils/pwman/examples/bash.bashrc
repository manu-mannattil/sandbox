#!/usr/bin/env bash
#
# A bunch of bash functions to make things easier.  Edit the variable
# $PWMAN_STORE as required.  This file must be sourced from ~/.bashrc.
#

export PWMAN_STORE=""  # Location of default password store

# Bash completion function for pwget(1)
_pwget() {
  if ! [ -f "$PWMAN_STORE" ]; then
    echo >&2 "pwget: unable to access password store"
    return 1
  else
    local cur="${COMP_WORDS[COMP_CWORD]}"
    local opts=$(sed -ne 's/^== \(.*\) ==$/\1/p' "$PWMAN_STORE")

    COMPREPLY=( $(compgen -W "${opts}" -- "${cur}") )
    return 0
  fi
}

complete -F _pwget pwget
