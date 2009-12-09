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


def pprint(wut, first=True):
  """More complex than the one below"""
  
  if isinstance(wut, MatchTracker):
    head = str(wut.rule)
    #wut.config._debug = False
    if head[-1] in '1234567890' and not wut.config._debug:
      head = ''
      for v in wut.value:
        head += pprint(v, first=False)
      while '  \n' in head:
        head = head.replace('  \n', ' \n')
      head = head.replace(' \n', '')
      return head+''
    head += ':'
    for v in wut.value:
      for line in pprint(v, first=False).split('\n'):
        head += '\n  '+line
    head += '\n'
    if first:
      while ' \n' in head: head = head.replace(' \n', '\n')
      while '\n\n' in head: head = head.replace('\n\n', '\n')
      return head.strip()
    return head
  return str(wut)+'\n'

'''
def __alt_pprint(wut):
  src = repr(wut)
  r = ''
  indent = 0
  tab = '  '
  src = src.replace(', ', ',').replace(':', '')
  for c in src:
    if c == '{':
      indent += 1
      r += '\n'+tab*indent
    elif c == '}':
      indent -= 1
    elif c == ',':
      r += '\n'+tab*indent
    else:
      r += c
  return r
'''

class MatchTracker:
  """
  A node in the parse tree. Each node coresponds to a rule. Each node keeps a list of accepted valsi
  """

  def __repr__(self):
    #if str(self.rule)[-1] in '1234567890' and self.accepted:
    if not self.config._debug and (len(self.value) == 1 and type(self.value[0]) == MatchTracker):
      return repr(self.value)[1:-1]
    r = str(self.rule)+':{'+repr(self.value)[1:-1]+'}' #+"*"*(not self.accepted) #XXX self.accepted is probably something horrible
    #if self.stack:
    #  r += '<'+str(self.stack)[1:-1]+'>'
    return r
  def __init__(self, valsi, rule, conf=None, current_valsi=0, parent=None, depth=0):
    assert conf
    self.config = conf
    self.value = []
    self.valsi = valsi
    self.start = current_valsi
    self.current_valsi = self.start
    self.parent = parent
    self.depth = depth
    self.rule = rule
    self.accepted = False
    self.stack = [] #For inner-rule grammarstuffins
  def accept_terminal(self):
    #print("adding terminal", self.valsi[self.current_valsi])
    self.value.append(self.valsi[self.current_valsi])
    self.current_valsi += 1
  def append_rule(self, rule):
    child = MatchTracker(self.valsi, rule, current_valsi=self.current_valsi, parent=self, depth=self.depth+1, conf=self.config)
    self.value.append(child)
    return child
  def accept_rule(self):
    assert self.value
    self.accepted = True
    self.current_valsi = self.value[-1].current_valsi  #+ 1
    #self.config.debug('ACCEPT', self)
  def fail(self):
    #A rule failed
    if self.parent:
      #if self.value:
      #self.config.debug("@@@ FAILING", self)
      self.parent.value.pop(self.parent.value.index(self))
      #self.parent.value.pop(self.start)
    else:
      raise Exception("Tried to fail root node")
  def finalize(self):
    #Kill the valsi???
    #return
    try:
      while self.current_valsi > 0:
        #print(self.current_valsi)
        self.current_valsi -= 1
        #print("Losing", self.valsi.pop())
    except (EOFError, StopIteration):
      return
  def checkin(self):
    """
    Append the current state onto a stack. This is for a rule's structure.
    """
    #self.config.debug("checkin")
    self.stack.append((self.current_valsi, list(self.value)))
    #self.config.debug('---', self.stack[-1])
  def checkout(self):
    """
    Something failed. Restore an old state from the stack
    """
    #self.config.debug("popping", self.stack)
    old_state = self.stack.pop()
    (self.current_valsi, self.value ) = old_state
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
    import sys
    while 1:
      root_rule = magic_bnf.Rule(self.config.parsing_unit)
      root_value = BNF[root_rule]
      tracker = MatchTracker(self.valsi, root_rule, conf=self.config)
      sys.tracker = tracker
      try:
        v = root_value.match(tracker)
      except (EOFError, StopIteration) as e:
        input("EXCEPTION: Hit the end (press enter)")
        raise e
      
      tracker.finalize()
      if v:
        tracker.accept_rule()
      else:
        break
      
      
      yield tracker
      #XXX Only do one for now
      break



def parse(string):
  main(Stream(Configuration(stdin=io.StringIO(string))))

def Stream(conf=None):
  if conf == None:
    conf = Configuration()
  de_debug = conf._debug
  conf._debug = False
  valsibuff = thaumatology.Stream(conf)
  treebuff = GrammarParser(valsibuff, conf)
  conf._debug = de_debug
  return Buffer(treebuff, conf)

def main(_stream):
  r = []
  #r = 
  #print('='*70)
  
  for i in _stream:
    #print('*************************\n', pprint(i), '\n-------------------------')
    print(pprint(i))
    r.append(i)
    #print(i)
  if not r:
    print(r, '(empty)')
  #if len(str(i)) < 33: #For testing. Didn't get much text.
    #raise SystemExit(1)
  if r:
    return r[0]
  


if __name__ == '__main__':
  r = main(Stream())
