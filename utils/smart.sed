#!/bin/sed -f
#% sed -nf % %
#
# smart.sed -- smart quotes, dashes, and ellipses in sed.
#
# Based on: http://www.leancrew.com/all-this/2010/11/smart-quotes-in-javascript/
#
# --------- TEST STRING ---------
#
#   Let's look at two apostrophe's [sic].
#   "'Let's try "nested" quotes,' he said."
#   Let's look at three apostrophes: won't, shouldn't.
#   A double quote--"within" dashes--would be nice.
#   A double quote--"within dashes"--would be nice.
#   I haven't tried ("parentheses" yet).
#   I haven't tried ("parentheses") yet.
#   What about "(parentheses)"?.
#   And "[brackets]"?.
#   I haven't tried ["brackets" yet].
#   I haven't tried ["brackets"] yet.
#   What about slashes/'virgules'?
#   What about slashes/"virgules"?
#   And {'curly' braces}?
#   And {"curly" braces}?
#   "'Twas the night before Christmas..." with a straight apostrophe—should fail.
#   "’Twas the night before Christmas…" with an explicit curly apostrophe.
#
# --------- TEST STRING ---------
#

/^# --------- TEST STRING ---------$/, /^# --------- TEST STRING ---------$/ {

  # Smarten quotes.
  s/\(^\|[-–—[:space:]\/{(\[\x22]\)\x27/\1‘/g
  s/\x27/’/g
  s/\(^\|[-–—[:space:]\/{(\[‘]\)\x22/\1“/g
  s/\x22/”/g

  # Smarten ellipses.
  s/\.\.\./…/g

  # Smarten dashes.
  s/---/—/g

  p
}
