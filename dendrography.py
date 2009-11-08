#!/usr/bin/python3.0
# -*- coding: utf-8 -*-

#import sys
#sys.setrecursionlimit(100)

from config import Configuration
from common import Buffer
import thaumatology
from bnf import BNF
import magic_bnf



class RuleList:
  #I think this is The One.
  def __repr__(self):
    return str(self.rule)+':'+repr(self.value)+"*"*(not self.accepted)
  def __init__(self, valsi, rule, current_valsi=0, parent=None):
    self.value = []
    self.valsi = valsi
    self.start = current_valsi
    self.current_valsi = self.start
    self.parent = parent
    self.rule = rule
    self.accepted = False
  def accept_terminal(self):
    print("adding terminal", self.valsi[self.current_valsi])
    self.value.append(self.valsi[self.current_valsi])
    self.current_valsi += 1
  def append_rule(self, rule):
    child = RuleList(self.valsi, rule, self.current_valsi, self)
    self.value.append(child)
    return child
  def accept_rule(self):
    assert self.value
    self.accepted = True
    self.current_valsi = self.value[-1].current_valsi  #+ 1
    print('ACCEPT', self)
  def fail(self):
    if self.parent:
      #if self.value:
      print("@@@ FAILING", self)
      self.parent.value.pop(self.parent.value.index(self))
      #self.parent.value.pop(self.start)
    else:
      raise Exception("Tried to fail root node")
  def finalize(self):
    #Kill the valsi???
    return
    while self.current_valsi >= 0:
      self.current_valsi -= 1
      self.valsi.pop()

class GrammarParser:
  def __init__(self, token_iter, config):
    self.valsi = token_iter
    self.config = config

  def __iter__(self):
    #yield ROOT_TOKENs
    while 1:
      #root = magic_bnf.Rule(self.config.parsing_unit) #BNF[self.config.parsing_unit]
      root_rule = magic_bnf.Rule(self.config.parsing_unit)
      root_value = BNF[root_rule]
      tracker = RuleList(self.valsi, root_rule)
      try:
        v = root_value.match(tracker)
      except (EOFError, StopIteration):
        raise Exception
      #except Exception as e:
        #print("Exception:", str(e), repr(e), type(e))
        #raise Exception
      
      #tracker.accept_rule()
      tracker.finalize()
      yield tracker
      ###if tracker.matches:
        ###print(tracker)
        ###for matcher in tracker.matches:
          ###print("Filling up", matcher)
          ###matcher.fill(self.valsi)
        ###yield tracker.matches
      ###else:
        ###matcher = Tracker.Match(BNF['unmatched'], 0, 1)
        ###matcher.fill(self.valsi)
        ###yield matcher
      #XXX Only do one for now
      break




def Stream(conf=None):
  if conf == None:
    conf = Configuration()
  valsibuff = thaumatology.Stream(conf)
  treebuff = GrammarParser(valsibuff, conf)
  return Buffer(treebuff, conf)


if __name__ == '__main__':
  r = tuple(Stream())
  if not r:
    print(r, '(empty)')
  for i in r:
    print(i)

