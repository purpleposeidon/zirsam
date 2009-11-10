# -*- coding: utf-8 -*-

"""
There are several modules with fancy latinesque names. Each handles a different phase of parsing, and they depend on a module below them. Each module functions independantly of the one above it

  orthography
      Converts arbitrary alphabets into latin. Then it determines the type of the letter. Then it groups the vowels and the consonants together.

  morphology
      Creates individual valsi using the BRKWORDS morphology algo

  thaumatology
      Does pre-processing for dendrography; it handles erasures, quoting, UI....

  dendrography
      Uses the BNF to create a parse tree, and then sorts it out to make it nice and pretty. The Magic words are (?) handled by the BNF... TODO see look uhm
  
  [As of writing, the modules below aren't implemented]
  
  semasiology
      Re-structures the tree. Changes pro-valsi to original values, check that selbri are real words

There are other files:
  config
      Handles command-line arguments, parser settings
  selmaho, tokens
      Creates token objects
  zirsam
      Will eventually be the main entry-point for everything, right now is uninteresting

"""

import sys

import config

#Contains the Buffer, a class used by every layer of the parser

class Buffer:
  #If this class used less methods, the stack would be shorter
  def __repr__(self):
    return "<Buffered {0}>".format(type(self.orig).__name__)
  def __init__(self, iterable, conf):
    if not hasattr(iterable, '__next__'):
      #raise Exception("Wrap in an iterator plz")
      self.orig = iterable
      iterable = iter(iterable)
    else:
      self.orig = iterable
    self.iterable = iterable
    self.buffer = []
    self.EOF = False
    self.config = conf

  def __feed_buffer(self):
    """Add a single item to the buffer"""
    if self.EOF:
      raise EOFError()
    try:
      self.buffer.append(self.iterable.__next__())
    except (EOFError, StopIteration) as e:
      self.config.debug("{0} got exception {1!r}".format(self, e))
      self.EOF = True
    finally:
      if self.EOF:
        raise EOFError()

  def __fill_to(self, index):
    while index + 1 > len(self.buffer):
      self.__feed_buffer()

  def insert(self, index, value):
    self.config.debug("Inserting {0} into {1}".format(value, index))
    if hasattr(value, 'position'):
      self.config.debug("(Originally located at {0})".format(value.position))
    self.__fill_to(index)
    if index > len(self.buffer):
      raise Exception("Can't insert item {0} at position {1} because that is at the end of the file".format(index, value))
    self.buffer.insert(index, value)

  def __iter__(self):
    i = 0
    while 1:
      try:
        yield self[i]
      except EOFError:
        break
      i += 1

  def items(self, num):
    self.__fill_to(num)
    return self.buffer[:num]

  def __getitem__(self, index):
    assert index >= 0
    self.__fill_to(index)
    return self.buffer[index]

  def pop(self, i=0):
    self.__fill_to(i)
    return self.buffer.pop(i)
  
  def end_zoi(self, token):
    return self.iterable.end_zoi()


class Position:
  #Stores information on which line/col/index a character is located at
  def __init__(self, _copy=None):
    if _copy:
      self.c = _copy.c
      self.col = _copy.col
      self.lin = _copy.lin
    else:
      self.c = 0
      self.col = 0
      self.lin = 0
  def __str__(self):
    return "Line {0}, Col {1}".format(self.lin, self.col)
  def __repr__(self):
    return '+{0}, {1}'.format(self.lin, self.col)
  def pushline(self):
    self.c += 1
    self.col = 0
    self.lin += 1
  def pushcol(self):
    self.c += 1
    self.col += 1


def Stream(conf=None):
  """
  This function will be found in each module that handles a level of parsing.
  Its job is to return a Buffer that will be used by the next client.
  This one doesn't actually do anything though. :P
  (Maybe it could return a stdin buffer? TODO)
  """
  if conf == None:
    conf = config.Configuration()
  pass

