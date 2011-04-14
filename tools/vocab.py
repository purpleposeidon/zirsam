#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Usage:
  ./tools/vocab.py [input file]
Reads lojban text from standard input, or from the input file. Writes to standard output how often a word occurs. If you want to sort this list, do:
  ./tools/vocab.py | sort -r

Output format is:
  (Number indicating word-count padded with at least a single zero) (word or rafsi) [optional note re. rafsi source]"""

import gc
import sys
import pickle
if "--help" in sys.argv:
  print(__doc__, file=sys.stderr)
  raise SystemExit

import zirsam
import zirsam.config as config
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

def run_bunch(stdin=None):
  c = config.Configuration(args=[], stdin=stdin)
  for word in morphology.Stream(conf=c):
    gc.collect()
    if isinstance(word, tokens.CMENE):
      continue #Ignore cmevla
    if isinstance(word, tokens.GARBAGE):
      continue #Ignore crap
    if not isinstance(word, tokens.BORING):
      if word.ve_lujvo_rafsi:
        for raf in word.ve_lujvo_rafsi:
          if len(raf) == 4 and raf[-1] == 'r':
            raf = raf[:3] #Chop out an r
          if len(raf) == 3:
            try:
              giz = rafsi[raf]
              add("{0} (rafsi of {1})".format(raf, giz))
            except:
              pass
      else:
        add(word.value)

if __name__ == '__main__':
  if len(sys.argv) == 2:
    stdin = open(sys.argv[1])
  else:
    stdin = None
  while 1:
    try:
      run_bunch(stdin=stdin)
    except Exception as e:
      sys.stderr.write(str(e)+'\n')
      continue
    except KeyboardInterrupt:
      break
    break
  for word in words:
    print('{0:0{2}} {1}'.format(words[word], word, len(str(top))+1))


