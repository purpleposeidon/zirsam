#!/usr/bin/python3.0
# -*- coding: utf-8 -*-

"""
INCOMPLETE

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

"""
This program's stdin/stdout will be formatted like:
11101101
00011111
It will be the responsibility of some other program to actually convert that, because python is stupid with that. I mean, yes, it could be done here. But no.

So, the typical lojban sentence has more cmavo than selbri. So, it should optimize for cmavo. 

So, here's the, uh, the grammar tree thing:
everything := (valsi)*
valsi :=
  1 #A cmavo or Escape
    1 #Escape
    0 #cmavo. 9 bits are used to pick the cmavo's index
  0 #A gismu
    

Let's start over. There are, I suppose, 1342 gismu and 792 cmavo.
So, what's the most efficient distribution of bit-space?
  1342 gismu requires 10 bits to count
    (194 numbers lost, which isn't very future-proof)
  792 cmavo requires 9 bits to count
    (231 numbers lost)
  2134 valsi require 11 bits to count
    (1961 numbers lost)

Now, we must consider the frequency of usage!
In a random paragraph from la .alis., I count 124 cmavo and 45 selbri, 154 whitespace and 2 cmene. (Should probably run it on the entire thing.... bah). Also, those selbri aren't gismu, which is what I'd be using for this simpler version.
But let us pretend that these numbers are typical.

So, there are 2.8 cmavo per selbri. There are different forms that could be used:
  Combine gismu and cmavo into one number
    11*3.8 = 41.8 bits
  Treat cmavo and gismu seperately
    2.8*9+10 = 35.2 bits
  In conclusion, treat them seperately.








If we include whitespace, we'll want it to be very compact!
  000   newline
  001   space
That's nice, only 3 bits.

"""


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
