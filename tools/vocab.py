#!/usr/bin/python3
"""Usage:
  ./tools/vocab.py
Reads lojban text from standard input. Writes to standard output how often a word occurs. If you want to sort this list, do:
  ./tools/vocab.py | sort -r

Output format is something like:
  {Number indicating word-count padded with at least a single zero} {word or rafsi} (optional note re. rafsi source)"""

import sys
import pickle
if len(sys.argv) > 1:
  print(__doc__, file=sys.stderr)
  raise SystemExit

import zirsam
import zirsam.morphology as morphology
import zirsam.tokens as tokens

rafsi_pick = zirsam.resource('r2g.pyk3')
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

def run_bunch():
  for word in morphology.Stream():
    if isinstance(word, tokens.CMENE):
      continue #Ignore cmevla
    if isinstance(word, tokens.GARBAGE):
      continue #Ignore crap
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

while 1:
  try:
    run_bunch()
  except:
    continue
  break
for word in words:
  print('{0:0{2}} {1}'.format(words[word], word, len(str(top))+1))
