#!/usr/bin/python3.0
# -*- coding: utf-8 -*-


from config import Configuration
from common import Buffer
import thaumatology
from bnf import BNF
import magic_bnf

class MatchWatch:
  def __init__(self, valsi_index):
    self.start = valsi_index
    self.end = None
    self.subrules = []


class Tracker:
  def __init__(self, valsi):
    self.valsi = valsi
    self.current_valsi = 0
    self.matches = []

  def begin(self):
    self.matches.append(MatchWatch(self.current_valsi))
  
  def end(self):
    self.matches[-1].end = self.current_valsi

  def add_rule(self):
    

class Tracker:
  class Node:
    def __init__(self, rule):
      """
      current_valsi....
      Node.begin()
        self.start = current_valsi
      Node.end()
        self.end = current_valsi
      Node.add_rule()
        self.internal_rules.append((current_valsi, rule))
      """
  class Match:
    #__slots__ = ("rule", "start", "end", "tokens")
    def __init__(self, rule, start, end):
      self.rule = rule
      self.start = start
      self.end = end
      self.tokens = None
    def fill(self, valsi):
      count = self.end - self.start
      self.tokens = []
      while count > 0:
        count -= 1
        self.tokens.append(valsi.pop())
    def __repr__(self):

      if self.tokens == None:
        return "{0}.match(???)".format(self.rule)
      return "{0}({1})".format(self.rule, self.tokens)
      #return "{0}({0})".format(self.rule, ' '.join(map(str, self.tokens)))

  def __repr__(self):
    return 'Tracker'+repr(self.matches)+'\n[extra]: '+repr(self.rule_matches)

  def __init__(self, valsi):
    self.valsi = valsi
    self.matches = [] #Using Tracker.Match objects
    self.current_rule = None
    self.current_valsi = 0 #An absolute offset!
    self.__start_valsi = 0
    self.rule_matches = []

  def save(self):
    print("saving", self.current_rule)
    #if self.current_valsi == 0:
      #raise Exception("Nothing happened!")

    self.matches.append(self.Match(self.current_rule, self.__start_valsi, self.current_valsi))
    self.__start_valsi = self.current_valsi+1
    self.current_rule = None

  def undo(self):
    if self.matches:
      old_match = self.matches.pop()
      self.current_rule, self.__start_valsi, self.current_valsi = old_match.rule, old_match.start, old_match.end


  def start(self, rule):
    self.current_rule = rule



class GrammarParser:
  def __init__(self, token_iter, config):
    self.valsi = token_iter
    self.config = config

  def __iter__(self):
    #yield ROOT_TOKENs
    while 1:
      root = magic_bnf.Rule(self.config.parsing_unit) #BNF[self.config.parsing_unit]
      tracker = Tracker(self.valsi)
      try:
        v = root.match(tracker)
      except Exception as e:
        print("Exception:", str(e), repr(e), type(e))
        raise
      if tracker.matches:
        print(tracker)
        for matcher in tracker.matches:
          print("Filling up", matcher)
          matcher.fill(self.valsi)
        yield tracker.matches
      else:
        matcher = Tracker.Match(BNF['unmatched'], 0, 1)
        matcher.fill(self.valsi)
        yield matcher
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
    print(r)
  for i in r:
    print(i)

