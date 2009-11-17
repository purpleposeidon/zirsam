#!/usr/bin/python3.0
# -*- coding: utf-8 -*-
#Create a dictionary mapping rafsi to gismu

src = '/usr/share/lojban/gismu.txt'
root = '../data/'

import pickle, os


src = open(src)
src.readline() #ur heder let meh kil it for u
" bacru         ba'u utter                                     x1 utters verbally/says/phonates/speaks [vocally makes sound] x2                                 1h 386    [also voices; does not necessarily imply communication or audience; ('says' is usually cusku)]; (cf. krixa, cusku, casnu, tavla, voksa, pinka)"
r_start = len(" bacru ")
r_end = len(" bacru         ba'u")

r2g = {}
g2r = {}
for line in src:
  gismu = line[1:6].strip()
  rafsi = line[r_start:r_end].strip().split(' ')
  if rafsi:
    for raf in rafsi:
      raf = raf.strip()
      r2g[raf] = gismu
    g2r[gismu] = rafsi

pickle.dump(r2g, open(os.path.join(root, 'r2g.pyk'), 'wb'))
pickle.dump(g2r, open(os.path.join(root, 'g2r.pyk'), 'wb'))