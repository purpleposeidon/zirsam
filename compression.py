#!/usr/bin/python3.0
# -*- coding: utf-8 -*-

"""
Compress or decompress lojban text using our special format.
Input text is the data represented as 1's and 0's, with a newline seperating each 8-bit byte.
Output is formatted the same.

It uses the contents of the data/ directory.

"""


import sys
import os

import config
import morphology

data_dir = os.path.join(os.getcwd(), sys.argv[0])
data_dir = os.path.join(data_dir, "data")




def compress():
  i = 0
  for x in sys.argv: #For config
    if x == '--compress':
      sys.argv.pop(i)
    i += 1
  
  conf = config.Configuration(sys.argv[1:])
  p = morphology.Stream(conf, sys.stdin)

def decompress():
  ...

if __name__ == '__main__':
  if '--compress' in sys.argv and not '--decompress' in sys.argv:
    compress()
  elif '--decompress' in sys.argv and not '--compress' in sys.argv:
    decompress()
  elif '--decompress' in sys.argv and '--compress' in sys.argv:
    print("Agh!")
  else:
    print("Usage:\n\t{0} --compress\n\t{0} --decompress".format(sys.argv[0]))
