#!/usr/bin/python3.0
# -*- coding: utf-8 -*-

class ParsingStructure:
  def __init__(self, token_stream):
    self.buffer = token_stream
    self.root = None

class Rule:
  def __init__(self, f):
    self.f = f

  def match(self, token_stream):
    

"""
Must be able to implement:
  sentence
    bridi
      se
      selbri
      co
    sumti
      lo
        selbri
"""

@rule
def document(parse_structure):
  