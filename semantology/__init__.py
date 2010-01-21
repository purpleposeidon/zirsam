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

from tracker_handler import examine, SemanticsException

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
    return """Abstractions:
{3}""".format(hex(id(self)), self.ki, self.koha, self.__abs_str__())
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
    #Creates a new abstraction, but doesn't push it onto the stack
    self.abstraction_count += 1
    a = Abstraction(self.abstraction_count)
    self.abstraction_list.append(a)
    return a

class Fact:
  def __init__(self, group, id_, selbri_type):
    self.group = group
    self.id = id_
    self.type = selbri_type
  def __repr__(self):
    if self.id == 0: value = "zo'e"
    else: value = self.id
    return "G{0} #{1} {2}".format(self.group, value, self.type)

class SelbriClass:
  SE_VALS = {'se':2, 'te':3, 've':4, 'xe':5}
  PA_VALS = {'1':'pa', '2':'re', '3':'ci', '4':'vo', '5':'mu', '6':'xa', '7':'ze', '8':'bi', '9':'so', '0':'no'}
  class SelbriType:
    def __init__(self, name, slot, truth_function):
      self.name = name #Some stupid string
      self.slot = slot
      self.truth_function = truth_function
      
  def __init__(self, name, max_slots=5, truth_function=None):
    self.name = name
    self.max_slots = max_slots
    self.truth_function = truth_function

  def access(self, SE=1):
    if SE in SelbriClass.SE_VALS:
      s = SelbriClass.SE_VALS[SE]
    elif SE == 1:
      s = ''
    else:
      assert SE >= 1
      s = 'xi'
      for digit in str(SE):
        s += SelbriClass.PA_VALS[digit]
    return SelbriClass.SelbriType(s+self.name, SE, self.truth_function)


class Abstraction:
  def __str__(self):
    #This is the most beautiful thing you've ever seen in your life.
    #And you know it.
    r = """  #{0}: {1} --> {2}"""
    return r.format(self.id,
      ' '.join(str(_) for _ in self.selbri),
      " gi'a ".join(_.repr(self) for _ in self.terms)
    )
    #return """  #{0}: {1} --> {2}""".format(self.id, ' '.join(str(_) for _ in self.selbri), ', '.join(str(_) for _ in self.terms))
  def refer(self):
    return self.get_term(1)
    #return "#"+str(self.id)
  def __init__(self, id_):
    self.id = id_
    assert type(self.id) == int
    self.terms = [] #terbri
    self.filled_places = [] #For FA terms
    self.selbri = [] #The first is the primary one, like in a tanru.
    self.SE = [] #Swap 1 with these values...
    self.observative = ... #Don't know
  def resolve_nei(self):
    selbri = self.selbri[0]
    for term in self.terms:
      #print(term, type(term))
      if term.type.value == 'nei' and term.abstraction == self:
        term.type = selbri
  def resolve_se(self):
    #while self.se:
    #swap x1 with x_(self.se.pop())
    selbri = self.selbri[0]
    while self.SE:
      x1 = self.get_term(1, selbri)
      SE = self.SE.pop(0)
      xSE = self.get_term(SE, selbri)
      x1.SE = SE
      if xSE:
        xSE.SE = 1
  def get_term(self, SE, type_=None):
    for term in self.terms:
      if SE == term.SE: #and type_ == term.type:
        return term
    #Uh oh, the term doesn't exist! Make something up.
    if not self.selbri:
      selbri = tokens.FakeToken(selmaho.GOhA, "nei")
    else:
      selbri = self.selbri[0]
    fakery = Terbri(self, SE, selbri, tokens.FakeToken(selmaho.KOhA, "zo'e"))
    self.terms.append(fakery)
    return fakery
  def next_term(self, tag_num=None):
    if tag_num:
      #Given a FA-index
      if tag_num > 5:
        raise SemanticsException("fai/fi'a not implemented")
      assert tag_num
      if tag_num in self.filled_places:
        print(tag_num, self.filled_places)
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
    if self.value == ...:
      v = "<Not yet known>"
    else:
      v = self.value.value
    return """{2} {0}{1}""".format(['wtf ', '', 'se ', 'te ', 've ', 'xe '][self.SE], self.type.value, v)
  def repr(self, from_):
    if from_.id!=self.abstraction.id:
      return "#{2}".format(['wtf ', '', 'se ', 'te ', 've ', 'xe '][self.SE], self.type.value, self.abstraction.id)
    else:
      return str(self)
  def __init__(self, abstraction, SE, type_, sumti):
    """3, se klama, <lo do zdani>"""
    self.abstraction = abstraction
    assert isinstance(self.abstraction, Abstraction) #DEBUG
    self.SE = SE #1 = nothing, 2 = se, 3 = te, ve = 4, xe = 5
    self.type = type_
    self.value = sumti

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



