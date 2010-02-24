#!/usr/bin/python3.0
# -*- coding: utf-8 -*-

#import os
#os.chdir('../')

import dendrography
import config
import tokens
import selmaho

from semantology.tracker_handler import examine, SemanticsException



class Tense:
  def __str__(self):
    return ''.join(self.ki)
  def __init__(self, ki=[]):
    self.ki = ki


class Context:
  def __repr__(self):
    return """Context at {0}:
KI status: {1}
KOhA status: {2}
Facts:
{3}""".format(hex(id(self)), self.ki, self.koha, self.__fact_str__())
  def __fact_str__(self):
    r = ''
    for a in self.facts:
      r += str(a) + '\n'
    return r
  def __init__(self):
    self.koha = {} #Would also include things like 'ta mlatu .i my klama lo do zdani'. The keys are Tokens
    self.ki = Tense()
    self.fact_stack = []
    
    self.selbri_stack = []
    self.term_type_stack = []
    self.se_stack = []
    self.group_stack = []
    
    self.facts = []
    self.groups = {}
    self.group_count = 0

  def __getitem__(self, group_id):
    return self.groups[group_id]

  def add_fact(self, referred_group, selbri_type, group_count=None):
    #assert type(referred_group) == int
    if not group_count:
      group_count = self.group_count
      self.group_count += 1
    a = Fact(group_count, referred_group, selbri_type)
    if group_count in self.groups:
      self.groups[group_count].append(a)
    else:
      self.groups[group_count] = [a]
    self.facts.append(a)
    return a

  def next_slot(self, group_id):
    #group = self.fact[group_id]
    #group = list(self.where(lambda fact: fact.group == group_id))
    group = self.groups.get(group_id)
    if not group:
      return 1
    print(group)
    end = group[-1].type.slot
    i = 0
    while 1:
      if group[i].type.slot == end:
        i = 0
        end += 1
      i += 1
      if i == len(group):
        break

    return end
  def assign_selbri(self, group_id, new_selbri):
    group = self.groups[group_id]
    for fact in group:
      slot = fact.type.slot
      fact.type = access(new_selbri, slot)
      if new_selbri.max_slots != -1 and slot >= new_selbri.max_slots:
        raise SemanticsException("Too many slots filled for this selbri")
  def where(self, lamb, group_id):
    if not group_id:
      for _ in self.facts:
        if lamb(_): yield _
    else:
      for _ in self.groups[group_id]:
        if lamb(_): yield _

class Fact:
  def __init__(self, group, referred_group, selbri_type):
    self.group = group
    self.referant = referred_group
    self.type = selbri_type
  def __repr__(self):
    if self.referant == 0: value = "zo'e"
    else: value = '#' + str(self.referant)
    return "#{0} {1} {2}".format(self.group, value, self.type)

class BridiManager:
  """
    Temporary handling of bridi...
  """
  def __init__(self):
    self.selbri = []
    self.terbri = {}
    self.se = []

  def add_term(self, value, FA=None):
    if not tag:
      

  def apply(self, context):
    assert self.selbri
    for se in self.se:
      


TYPES = {}
SE_VALS = {'se':2, 'te':3, 've':4, 'xe':5}
PA_VALS = {'1':'pa', '2':'re', '3':'ci', '4':'vo', '5':'mu', '6':'xa', '7':'ze', '8':'bi', '9':'so', '0':'no'}

class SelbriClass:
  class SelbriType:
    def __init__(self, name, slot, truth_function):
      self.name = name #Some stupid string
      self.slot = slot
      self.truth_function = truth_function
    def __repr__(self):
      return self.name
    def __str__(self):
      return self.name
  
  def __init__(self, name, max_slots=5, truth_function=None):
    self.name = name
    self.max_slots = max_slots
    self.truth_function = truth_function
    TYPES[name] = self
  def __repr__(self):
    return str(self.name)
  def access(self, SE=1):
    if SE in SE_VALS:
      s = SE_VALS[SE]
    elif SE == 1:
      s = ''
    elif SE == 0:
      raise SemanticsException("sexino? What?") #Ha ha. Sex. I no.
    else:
      s = 'xi'
      for digit in str(SE):
        s += PA_VALS[digit]
    if self.max_slots != -1 and SE > self.max_slots:
      print("You want", SE, "have only", self.max_slots)
      raise SemanticsException("This mamtabedo doesn't have that many slots")
    return SelbriClass.SelbriType(s+self.name, SE, self.truth_function)


SelbriClass("<zasti>", max_slots=1)
SelbriClass("<unknown>", max_slots=-1)

def access(val, *args, **kwargs):
  try:
    return TYPES[val].access(*args, **kwargs)
  except KeyError:
    return SelbriClass(val, max_slots=-1)
