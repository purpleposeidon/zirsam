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
  for value in tracker.value:
    if isinstance(value, dendrography.MatchTracker):
      examine(value, context)
  if hasattr(tracker_handler, end_name):
    getattr(tracker_handler, end_name)(tracker, context)


#--------------- Semantics Bits Handlers ---------------


def pre_sentence(tracker, context):
  context.push_abstraction()
def end_sentence(tracker, context):
  context.pop_abstraction()

def pre_tanru_unit_2(tracker, context):
  selbri = tracker.node.get("SELBRI")
  if not selbri:
    raise SemanticsException("Can only handle SELBRI right now, but tanru_unit_2 consists of {0}".format(tracker.node))
  context.abstraction_stack[0].selbri.insert(0, selbri)
def end_tanru_unit_2(tracker, context): pass

def pre_bridi_tail(tracker, context):
  obs = context.abstraction_stack[-1].observative
  if obs == ...:
    context.abstraction_stack[-1].observative = True
def end_bridi_tail(tracker, context): pass


def pre_term(tracker, context):
  FA = tracker.node.get("FA")
  if FA:
    FA = selmaho.FA.forms.index(FA.value)
  term_num = context.abstraction_stack[-1].next_term(FA)
  new_term = semantology.Terbri(context.abstraction_stack[-1], term_num, "nei", ...)
  context.abstraction_stack[-1].terms.append(new_term)
  
def end_term(tracker, context): pass


def pre_sumti_6(tracker, context):
  context.abstraction_stack[-1].terms[-1].sumti = tracker.value[0]
  
def end_sumti_6(tracker, context): pass