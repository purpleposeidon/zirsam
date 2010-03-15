#!/usr/bin/python3
#Doesn't take into account si & friends; you could use thaumatology, but then "zo ka" would be treated as 1 word.
import sys
sys.path.append('./')
import morphology
import tokens
i = 0
for _ in morphology.Stream():
  if not isinstance(_, tokens.IGNORABLE):
    i += 1
print(i)
