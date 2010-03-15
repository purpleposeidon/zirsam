#!/usr/bin/python3
"""Usage:
  ./tools/vocab.py
Reads lojban text from standard input. Writes to standard output how often a word occurs. If you want to sort this list, do:
  ./tools/vocab.py | sort -r"""

import sys
import pickle
if len(sys.argv) > 1:
  print(__doc__, file=sys.stderr)
  raise SystemExit

sys.path.append('./')
import morphology
import tokens

rafsi_pick = 'data/r2g.pyk3'
rafsi = pickle.load(open(rafsi_pick, 'rb'))
words = {}
top = 0

def add(word):
  if word in words:
    words[word] += 1
  else:
    words[word] = 1
  global top
  top = max(words[word], top)


for word in morphology.Stream():
  if isinstance(word, tokens.CMENE):
    continue #Ignore cmevla
  if not isinstance(word, tokens.BORING):
    if word.ve_lujvo_rafsi:
      for raf in word.ve_lujvo_rafsi:
        if len(raf) == 4:
          raf = raf[:3] #Chop out an r
        if len(raf) == 3:
          try:
            giz = rafsi[raf]
            add("{0} (rafsi of {1})".format(raf, giz))
          except:
            pass
    else:
      add(word.value)
for word in words:
  print('{0:0{2}} {1}'.format(words[word], word, len(str(top))+1))
