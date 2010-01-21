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

NoExamine = object() #Don't run examine() on the node's sub-children.

def examine(tracker, context):
  pre_name = "pre_"+tracker.rule.name
  end_name = "end_"+tracker.rule.name
  if hasattr(tracker_handler, pre_name):
    special = getattr(tracker_handler, pre_name)(tracker, context)
    if special == NoExamine:
      return
    #print(pre_name, context)
  for value in tracker.value:
    if isinstance(value, dendrography.MatchTracker):
      examine(value, context)
  if hasattr(tracker_handler, end_name):
    getattr(tracker_handler, end_name)(tracker, context)
    #print(end_name, context)

SE_VALS = {'se':2, 'te':3, 've':4, 'xe':5}
#TODO : It would be nice to have a checker to make sure you've spelled your function names correctly.
#Err.
#ni'o http://www.lojban.org/tiki/BPFK+Section:+gadri
#--------------- Semantics Bits Handlers ---------------


def pre_sentence(tracker, context):
  context.push_abstraction()
def end_sentence(tracker, context):
  context.pop_abstraction()

def pre_tanru_unit_2(tracker, context):
  selbri = tracker.node.get("BRIVLA")
  if selbri:
    context.abstraction_stack[0].selbri.insert(0, selbri)
    #If we don't get a selbri now, hopefully we'll get one later. Otherwise, no selbri = emo
  if tracker.node.get("SE"):
    se_item = SE_VALS[tracker.node['SE'].value]
    context.abstraction_stack[0].SE.append(se_item)
def end_tanru_unit_2(tracker, context): pass

def pre_bridi_tail(tracker, context):
  obs = context.abstraction_stack[0].observative
  if obs == ...:
    context.abstraction_stack[0].observative = True
def end_bridi_tail(tracker, context): pass


def pre_term(tracker, context):
  FA = tracker.node.get("FA")
  if FA:
    FA = selmaho.FA.forms.index(FA.value)
    FA += 1
    print("Have FA:", FA)
  term_num = context.abstraction_stack[0].next_term(FA)
  new_term = semantology.Terbri(context.abstraction_stack[0], term_num, tokens.FakeToken(selmaho.GOhA, "nei"), ...)
  context.abstraction_stack[0].terms.append(new_term)
  
def end_term(tracker, context): pass


def pre_sumti_6(tracker, context):
  KOhA = tracker.node.get("KOhA")
  LU = tracker.node.get("LU")
  if KOhA:
    context.abstraction_stack[0].terms[-1].value = KOhA
  elif LU:
    text = tracker.node.get("text")
    context.abstraction_stack[0].terms[-1].value = text
    return NoExamine
  elif tracker.node.get("sumti_tail"):
    pass
  else:
    raise SemanticsException("Unable to do anything with this sumti_6 {0}".format(tracker))
  #context.abstraction_stack[0].terms[-1].value = tracker.value[0]
  
def end_sumti_6(tracker, context): pass

def pre_tail_terms(tracker, context): pass
def end_tail_terms(tracker, context):
  if context.abstraction_stack[0].selbri:
    context.abstraction_stack[0].resolve_nei() #Give our sumti's proper selbri
    context.abstraction_stack[0].resolve_se() #Deal with like xe se broda
  

def pre_sumti_tail_1(tracker, context):
  '''
Create a new abstraction
Add a terbri to the abstraction
The value of {the current terbri of the old abstraction} is the new terbri
  '''
  sumti_tail_abstraction = context.add_abstraction()
  #context.abstraction_stack[0].terms[0].value = sumti_tail_abstraction.refer()
  context.push_abstraction(sumti_tail_abstraction)
  #The abstraction of broda in {le broda} needs to have a zo'e
  fa_num = context.abstraction_stack[0].next_term()
  #fa_num oughta be 1!
  assert fa_num == 1
  new_term = semantology.Terbri(context.abstraction_stack[0], fa_num, tokens.FakeToken(selmaho.GOhA, "nei"), tokens.FakeToken(selmaho.KOhA, "zo'e"))
  sumti_tail_abstraction.terms.append(new_term)
  #input()
  
def end_sumti_tail_1(tracker, context):
  context.abstraction_stack[0].resolve_nei()
  context.abstraction_stack[0].resolve_se()
  sumti_tail_abstraction = context.pop_abstraction()
  context.abstraction_stack[0].terms[-1].value = sumti_tail_abstraction.terms[0]
  
