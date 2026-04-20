#!/bin/sh
#
# -----------  -----------------------------------------------------------
#        file  fix-email-date.sh
# description  Change the modification date (the one that you see in `ls -l')
#              of email to the first date found in the header.
#     created  2015-01-04 01:40 IST
#    modified  2015-01-04 01:40 IST
# -----------  -----------------------------------------------------------
#
# Usage: fix-email-date.sh <file>...
#
# This is extremely useful to fix email timestamps in Gmail.  If you've
# modified files in a maildir locally, then Gmail might screw up the
# timestamps and you'll end up seeing old messages marked as new.  Run
# this script like:
#
#   $ find .../path/to/maildir -type f -exec fix-email-date.sh {} +
#


[ $# -eq 0 ] && echo >&2 "usage: fix-email-date.sh <file>..." && exit 1

for m in "$@"; do
  dt=$(grep '^Date:' "$m" | head -n 1 | sed 's/^Date:[[:space:]]*//')

  if [ -z "$dt" ]; then
    echo >&2 "fix-email-date.sh: no date in '$m'"
  else
    ts=$(date --date="$dt" +%Y%m%d%H%M 2>/dev/null)
    touch -t "$ts" "$m"
  fi
done
