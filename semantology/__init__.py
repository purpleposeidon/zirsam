#!/usr/bin/python3.0
# -*- coding: utf-8 -*-

#import os
#os.chdir('../')
import sys
sys.path.append('./')

import dendrography
import config
import tokens
import selmaho

from tracker_handler import examine

"""
Steps...
  So, we make a handle_NODE for each node-type.
    Jeeze, maybe there should be something else...
  Right, so, we shouldn't use python code, we should use... like, a text file or something.
"""


class Tense:
  def __str__(self):
    return ''.join(self.ki)
  def __init__(self, ki=[]):
    self.ki = ki

class Context:
  def __str__(self):
    return """Context at {0}:
KI status: {1}
KOhA status: {2}
Abstractions:
{3}""".format(hex(id(self)), self.ki, self.koha, self.__abs_str__())
  def __abs_str__(self):
    r = ''
    for a in self.abstraction_list:
      s = str(a)
      if a in self.abstraction_stack:
        s = s.replace('\n', "(#{0})\n".format(self.abstraction_list.index(a)), 1)
      r += s + '\n'
    return r
  def __init__(self):
    self.koha = {} #Would also include things like 'ta mlatu .i my klama lo do zdani'. The keys are Tokens
    self.ki = Tense()
    self.abstraction_count = 0
    self.abstraction_stack = []
    self.abstraction_list = []

  def push_abstraction(self, a=None):
    if not a:
      a = self.add_abstraction()
    self.abstraction_stack.insert(0, a)

  def pop_abstraction(self):
    return self.abstraction_stack.pop(0)
  
  def add_abstraction(self):
    self.abstraction_count += 1
    a = Abstraction(self.abstraction_count)
    self.abstraction_list.append(a)
    return a


class Abstraction:
  def __str__(self):
    return """  #{0}: {1} --> {2}""".format(self.id, ' '.join(str(_) for _ in self.selbri), ', '.join(str(_) for _ in self.terms))
  def __init__(self, id_):
    self.id = id_
    self.terms = [] #terbri
    self.filled_places = [] #For FA terms
    self.selbri = [] #The first is the primary one, like in a tanru.
    self.observative = ... #Don't know
  def next_term(self, tag_num=None):
    if tag_num:
      #Given a FA-index
      if tag_num > 5:
        raise SemanticsException("fai/fi'a not implemented")
      assert tag_num
      if tag_num in self.filled_places:
        raise SemanticsException("Trying to double-dip a term")
      self.filled_places.append(tag_num)
    elif not self.filled_places:
      if self.observative == ...:
        #We don't know if it's an observative as we haven't hit bridi-tail yet.
        #Just kidding, we do, since there's a term. So, a term before bridi_tail.
        self.observative = False
        tag_num = 1
      elif self.observative == True:
        #Start at 2
        tag_num = 2
      else:
        raise Exception("Is this an observative? Okay, so self.observative = False. But, self.filled_places is empty.")
    else:
      tag_num = self.filled_places[-1]+1
      while tag_num in self.filled_places:
        tag_num += 1
        if tag_num == 5:
          raise SemanticsException("Number of terms went out of bounds") #nei fu ko'u fo'a
    self.filled_places.append(tag_num)
    return tag_num

class Terbri:
  def __str__(self):
    return """{0}{1}: {2}""".format(['wtf ', '', 'se ', 'te ', 've ', 'xe '][self.SE], self.type, self.sumti)
  def __init__(self, abstraction_id, SE, type_, sumti):
    """3, se klama, <lo do zdani>"""
    self.abstraction_id = abstraction_id
    self.SE = SE #1 = nothing, 2 = se, 3 = te, ve = 4, xe = 5
    self.type = type_
    self.sumti = sumti

class runterbri:
  """
    runterbri - artificial terbri
  whatsit do?
  A runterbri is something that is like computer-generated. Used to sumti-ize things that aren't really sumti, like tense, ACL, author, truth-value, existence
  Actually, this class is just so that we can have a pretty str()
  """
  def __init__(self, func):
    self.func = func
  def __str__(self):
    return "fi'o mezoirunterbri.{0}.runterbri".format(self.func.__name__)
  def __call__(self, *args, **kwargs):
    self.func(*args, **kwargs)
    
@runterbri
def exists(my, context):
  #Empty
  pass

@runterbri
def tense(my, context):
  assert isinstance(my, Tense)

@runterbri
def ACL(my, context):
  do = context.koha.get['do']
  if not do:
    raise Exception("do mo")
  if my.value != do.value:
    raise Exception("Permission denied.") # TODO: Groups

@runterbri
def truth(my, context):
  assert my in tokens.selmaho.NA

@runterbri
def author(my, context):
  #What to do? Check for existence?
  pass



