#!/bin/sed -nf
#
#% sed -nf % %
#
# -----------  -----------------------------------------------------------
#        file  xml2utf8.sed
# description  Convert XML entities to UTF8
#     created  2014-02-22 XX:XX IST
#    modified  2014-12-31 00:18 IST
# -----------  -----------------------------------------------------------
#
# --------- TEST STRING -------
#
#  Ampersand      &amp;
#  Quote          &quot;
#  Apostrophe     &apos;
#  Less than      &lt;
#  Greater than   &gt;
#
# --------- TEST STRING -------
#

/^# --------- TEST STRING -------$/, /^# --------- TEST STRING -------$/ {
  s/&amp;/\x26/g
  s/&quot;/\x22/g
  s/&apos;/\x27/g
  s/&lt;/\x3C/g
  s/&gt;/\x3E/g

  p
}

#
# AWK equivalent:
#
#   gsub("&amp;", "\\&")
#   gsub("&apos;", "'")
#   gsub("&gt;", ">")
#   gsub("&lt;", "<")
#   gsub("&quot;", "\"")
#
