#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Replace pronouns in a parse tree with references to what they refer to
"""
import weakref

import zirsam.dendrography

class XiRef:
  def __init__(self, xilist, index):
    self.xilist = xilist
    self.index = index
  
  def __call__(self):
    return list.__getitem__(self.xilist, index)

class XiList(list):
  def __init__(self):
    list.__init__(self)
    self.offset = 0
  def __getitem__(self, k):
    return XiRef(self, self.offset - k)
  def __call__(self):
    return self[0]()

def sequence(base):
  return [base.replace('V', _) for _ in 'aeiou']

class ProValsi:
  def __init__(self):
    self.koha = {}
    for v in ["mi", "do"] \
    + ["mi'o", "mi'a", "ma'a", "do'o"] \
    + ["da", "de", "di"] \
    + sequence("ko'V")+sequence("fo'V"): #XXX Ignoring other KOhA for now
      self.koha[v] = XiList()
      #It is likely that "KOhA xi" will be rarely used.
    self.goha = {}



def Evaluate(config=None):
  parse_iter = zirsam.dendrography.Stream(conf=config)
  for parse in parse_iter:
    pass

if __name__ == '__main__':
  print(Evaluate())