# -*- coding: utf-8 -*-

"""
The comment below contains code to generate a functions for everything.
First the pre_handle function is called. Then the functions for the sub-nodes are called.
Then the end_handle function is called.
"tracker" is a dendrography.MatchTracker object, context is semantics.foo.Context

It might be better to, instead of having ALL of those MANY empty functions, to just test to see if the function is  listed in the dictionary, or something. Maybe check for presence in a module, or something.
"""

"""
Okay, here's what's going down...
We need a function for TERM. It adds the place to an empty shell-thing...
We'll need a few functions for... sentence, tanru_unit. But let's do one thing at a time.
ko'a broda ko'e ko'i ko'o ko'u
fa ko'a broda fe ko'e fi ko'i fo ko'o fu ko'u

lo broda cu brode lo brodi lo brodo lo brodu
ko'a broda be ko'e bei ko'i be'o ko'u
lo broda be ko'e be'o cu brode

la djan goi ko'a cu barda .i ko'a mlatu
"""


import dendrography
import tokens
import selmaho

import sys
sys.path.append("./semantology")
import semantology
import tracker_handler

class SemanticsException(Exception): pass

def examine(tracker, context):
  pre_name = "pre_"+tracker.rule.name
  end_name = "end_"+tracker.rule.name
  if hasattr(tracker_handler, pre_name):
    getattr(tracker_handler, pre_name)(tracker, context)
    #print(pre_name, context)
  for value in tracker.value:
    if isinstance(value, dendrography.MatchTracker):
      examine(value, context)
  if hasattr(tracker_handler, end_name):
    getattr(tracker_handler, end_name)(tracker, context)
    #print(end_name, context)

SE_VALS = {'se':2, 'te':3, 've':4, 'xe':5}
#--------------- Semantics Bits Handlers ---------------


def pre_sentence(tracker, context):
  context.push_abstraction()
def end_sentence(tracker, context):
  context.pop_abstraction()
