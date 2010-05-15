#!/usr/bin/python3
#Doesn't take into account si & friends; you could use thaumatology, but then "zo ka" would be treated as 1 word.
import zirsam.morphology
import zirsam.tokens
i = 0
for _ in zirsam.morphology.Stream():
  if not isinstance(_, zirsam.tokens.IGNORABLE):
    i += 1
print(i)
