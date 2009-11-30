#!/usr/bin/python3.0
# -*- coding: utf-8 -*-

#import sys
#sys.setrecursionlimit(100)
import io

from config import Configuration
from common import Buffer
import thaumatology
from bnf import BNF
import magic_bnf



class MatchTracker:
  """
  A node in the parse tree. Each node coresponds to a rule. Each node keeps a list of accepted valsi
  """
  def __repr__(self):
    #if str(self.rule)[-1] in '1234567890' and self.accepted:
    if not self.config._debug and (len(self.value) == 1 and type(self.value[0]) == MatchTracker):
      return repr(self.value)[1:-1]
    r = str(self.rule)+':'+repr(self.value)+"*"*(not self.accepted)
    #if self.stack:
    #  r += '<'+str(self.stack)[1:-1]+'>'
    return r
  def __init__(self, valsi, rule, conf=None, current_valsi=0, parent=None):
    assert conf
    self.config = conf
    self.value = []
    self.valsi = valsi
    self.start = current_valsi
    self.current_valsi = self.start
    self.parent = parent
    self.rule = rule
    self.accepted = False
    self.stack = [] #For inner-rule grammarstuffins
  def accept_terminal(self):
    #print("adding terminal", self.valsi[self.current_valsi])
    self.value.append(self.valsi[self.current_valsi])
    self.current_valsi += 1
  def append_rule(self, rule):
    child = MatchTracker(self.valsi, rule, current_valsi=self.current_valsi, parent=self, conf=self.config)
    self.value.append(child)
    return child
  def accept_rule(self):
    assert self.value
    self.accepted = True
    self.current_valsi = self.value[-1].current_valsi  #+ 1
    print('ACCEPT', self)
  def fail(self):
    #A rule failed
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
  def checkin(self):
    """
    Append the current state onto a stack. This is for a rule's structure.
    """
    print("checkin")
    self.stack.append((self.current_valsi, list(self.value)))
    print('---', self.stack[-1])
  def checkout(self):
    """
    Something failed. Restore an old state from the stack
    """
    print("popping", self.stack)
    old_state = self.stack.pop()
    (self.current_valsi, self.value ) = old_state
    #print("checkout")
  def commit(self):
    """
    Something succeeded. Remove from stack
    """
    #print("commit")
    self.stack.pop()


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
      tracker = MatchTracker(self.valsi, root_rule, conf=self.config)
      try:
        v = root_value.match(tracker)
      except (EOFError, StopIteration) as e:
        raise e
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


def parse(string):
  main(Stream(Configuration(stdin=io.StringIO(string))))

def Stream(conf=None):
  if conf == None:
    conf = Configuration()
  valsibuff = thaumatology.Stream(conf)
  treebuff = GrammarParser(valsibuff, conf)
  return Buffer(treebuff, conf)

def main(_stream):
  r = tuple(_stream)
  #print('='*70)
  if not r:
    print(r, '(empty)')
  for i in r:
    print(i)
  return len(str(i)) < 33 #For testing. Didn't get much text.
    


if __name__ == '__main__':
  if main(Stream()):
    raise SystemExit(1)
