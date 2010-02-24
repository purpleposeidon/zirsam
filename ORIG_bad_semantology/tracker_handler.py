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
FA_VALS = {'fa':1, 'fe':2, 'fi':3, 'fo':4, 'fu':5}
#TODO : It would be nice to have a checker to make sure you've spelled your function names correctly.
#Err.
#ni'o http://www.lojban.org/tiki/BPFK+Section:+gadri
#--------------- Semantics Bits Handlers ---------------

def pre_sentence(tracker, context):
  context.group_count += 1
  context.group_stack.append(context.group_count)
  context.selbri_stack.append(semantology.TYPES["<unknown>"])
  context.term_type_stack.append(1)
  

def pre_term(tracker, context):
  fa = tracker.node.get("FA")
  if fa:
    # TODO Also fi'a and fai
    index = FA_VALS[fa]
    subscript = tracker.pull("free", "xi", "number")
    if subscript:
      raise Exception("TODO: Function for turning [Number, ki'o, Tokens, Into, a] real number")
  else:
    #Advance to the next unused slot
    index = context.next_slot(context.group_stack[-1])
  context.term_type_stack[-1] = index

def pre_sumti_6(tracker, context):
  if tracker.node.get("KOhA"):
    koha = tracker.node['KOhA'].value
    #Look it up in our context...
    if not koha in context.koha:
      zasti = context.add_fact(0, semantology.access("<zasti>")).group
      context.koha[koha] = zasti
    else:
      zasti = context.koha[koha]
    context.add_fact(zasti, semantology.access("<unknown>"))
  elif tracker.node.get("LE"):
    le = tracker.node['LE'].value
    

def pre_selbri(tracker, context):
  context.selbri_stack[-1] = '' #No longer unknown, now we're figuring it out


def pre_tanru_unit_2(tracker, context):
  se = tracker.node.get("SE")
  if se:
    context.se_stack.append(SE_VALS[se])
  brivla = tracker.node.get("BRIVLA")
  if brivla:
    context.selbri_stack[-1] += ' ' + brivla.value
    return
  nu = tracker.node.get("NU")
  if nu:
    context.selbri_stack[-1] += ' '+brivla.text() # XXX This says that {nusesebroda} != {nubroda}
    return NoExamine

#def end_selbi(tracker, context):
  #context.selbri_stack[-1] = context.selbri_stack[-1].strip()

def end_sentence(tracker, context):
  groupid = context.group_stack.pop()
  selbri = context.selbri_stack.pop().strip()
  context.assign_selbri(groupid, semantology.access(selbri))
  
  while context.se_stack:
    se = context.se_stack.pop()
    pull = context.where(lambda fact: fact.type.slot == se, groupid)
    shift = context.where(lambda fact: fact.type.slot == 1, groupid)
    pull.slot = 1
    shift.slot = se