#!/usr/bin/python3.0
# -*- coding: utf-8 -*-
"""
Use the BNF data to assemble a parse tree


A thought:
  When there is an error parsing (and we are not strict), don't start crying! Fold that garbage into the parent node! lo nu mi tavla xfyweflkglez do cu se nelci do
  nelci
    (se)
    lo
      nu
        tavla
          mi
          ERROR(xfwerflzdf)
          do
    do
"""

import sys

from config import Configuration
import morphology
from bnf import BNF

REVERSE_BNF = {}
for key in BNF:
  rule = BNF[key]
  REVERSE_BNF[rule] = key

ROOT_TOKEN = "sentence" #Todo: Put this in the Configuration



class Node:
  def __init__(self):
    pass


class GrammarParser:
  def __init__(self, token_iter, config):
    self.valsi = token_iter
    self.config = config

  def parse(self):
    """
    Parse everything at once, make a big tree
    """

  def parse_to(self, top_rule):
    """When the rule "top_rule" has been fullfilled, return the value."""

  def __iter__(self):
    """
    yield ROOT_TOKENs
    """
    valsi_index = 0
    
    """How is this going to work? Yield sentences? Add more items to the tree? Yield branches?
    Think about downstream, what is it going to want? It's going to want... sentences?
    Hmmm. But, of course, the BNF makes that somewhat difficult. It may be necessary to exclude some rules.

    So, then, which rules are excluded? I don't like this, because then I would have to do hard haxxing to the language
    Okay
    Yield branches.
    ahhh....
    Okay. So you yield nodes, which would themselves yield more nodes. So, if you wanted only the entire text, you'd just directly do
    iter(TreeParser)
    But, if you wanted the niho's, sentences...
    for _ in TreeParser:
      iter(_.NIhO)

    Well, maybe you could have ahhh
    Okay. I've got it. You can't iterate this thing directly, that would be way too insane, as it's a fucking tree, iterating a tree would just give you the leaves. So, what you want to do is iterate over specific branches. Say, "I want all of the sentence branches" or, "I want all of the sections"
    or, "I want all of the sumti"

    Well, firstly, what's a program that might use this? The re-structurer. It wants sentences... it wants...

    Well, what would be the best way to do that?
      text
        section
          sentence
    Could create different kinds of parsers.

    Ideas for using this:
      Semantical analysis
      Restructuring

    Well, there are two types of applications, right?
        "I want all of it at once"
    and
        "I am real-time, so I need stuff when I can get it"
    For now, let us just write something that parses everything at once. Then we can figure out something that fits in better with the rest of the layers.
    """
    ...


def Stream(config, stdin):
  valsibuff = morphology.Stream(config, stdin)
  treebuff = GrammarParser(valsibuff, config)
  return treebuff

if __name__ == '__main__':
  config = Configuration()
  
  p = Stream(config, sys.stdin)
  for i in p:
    print(i)
'''
So...
we get the rule with the longest match! Okay, so then we have that 'rule'. Now we have to match 'rule'+following token.

Except that there shouldn't be a 'longest match', it should be the only match!


well, anyways. What's the easiest? What seems obvious to me, I suppose.  So, the bottom-up approach?

Well, Top-Down would make it easier to break at sentences or something...
How about this: "seperating values"
Ah! I like that! Okay, so, when we reach a ROOT_TOKEN, we don't go up any farther. So, for now, ROOT_TOKEN = "sentence"
'''