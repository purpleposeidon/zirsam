#!/usr/bin/python3.0
# -*- coding: utf-8 -*-

"""
orthography.py - Handle the messy, dirty stuff of input.

This file handles the inputting of text, and the classification and grouping of characters.
"""
import sys


class Position:
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


class Buffer:
  def __repr__(self):
    return "<Buffered {0}>".format(self.iterable)
  def __init__(self, iterable, config):
    self.iterable = iterable
    self.buffer = []
    self.EOF = False
    self.config = config
  
  def __feed_buffer(self):
    """Add a single item to the buffer"""
    if self.EOF:
      raise EOFError()
    try:
      self.buffer.append(self.iterable.__next__())
    except (EOFError, StopIteration) as e:
      if self.config.debug:
        print(self, "got eof error:", e, file=sys.stderr)
      self.EOF = True
    finally:
      if self.EOF:
        raise EOFError()
  
  def __fill_to(self, index):
    while index + 1 > len(self.buffer):
      self.__feed_buffer()
  
  def insert(self, index, value):
    if self.config.debug:
      print("Inserting {0} into {1}".format(value, index), file=sys.stderr)
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



class Character:
  
  
  
  def clean_val(v):
    #Escapes stuff if neccessary. "\n" -> "\\n"
    if '\\' in repr(v):
      return repr(v)[1:-1]
    else:
      return str(v)
  
  def __repr__(self):
    return str(self)
    #return "<{0} {1}>".format(self.value, self.position)
  
  def __str__(self):
    return Character.clean_val(self.value)
  
  def __init__(self, c, position, config):
    self.original = c
    
    assert position != None
    self.position = position
    
    self.accented = False
    self.V = False
    self.C = False
    self.y = False
    self.comma = False
    self.period = False
    self.h = False
    self.whitespace = False
    self.garbage = False
    self.EOF = False
    
    charset = config.charset
    
    
    if c in charset.eof:
      self.EOF = True
      self.value = ''
    elif c in charset.accent_vowel:
      if c in charset.A: self.value = 'A'
      elif c in charset.E: self.value = 'E'
      elif c in charset.I: self.value = 'I'
      elif c in charset.O: self.value = 'O'
      elif c in charset.U: self.value = 'U'
      else: wtf
      self.accented = True
      self.V = True
    elif c in charset.low_vowel:
      self.value = c
      self.V = True
    elif c.lower() in charset.con:
      self.value = c.lower()
      self.C = True
    elif c in charset.y:
      self.value = 'y'
      self.y = True
    elif c in charset.comma: 
      self.value = ','
      self.comma = True
    elif c in charset.period:
      self.value = '.'
      self.period = True
    elif c in charset.h:
      self.value = "'"
      self.h = True
    elif c in charset.whitespace:
      self.value = c
      self.whitespace = True
    else:
      self.garbage = True
      self.value = c
    self.value

def stream_char(fd, config):
  #XXX TODO: Use EncodingTable
  p = Position()
  while 1:
    c = fd.read(1)
    if c == '\n':
      p.pushline()
    elif c:
      p.pushcol()
    
    if c in config.charset.eof:
      yield Character('', Position(p), config)
      break
    else:
      yield Character(c, Position(p), config)

def stream_bit(fd):
  while 1:
    if fd.EOF:
      break
    yield Bit(fd)

class Bit:
  def __len__(self):
    return len(self.chars)
  def __str__(self):
    r = ''
    for c in self.chars:
      r += c.original
    return r
  def __getitem__(self, index):
    return self.chars[index]
  def __repr__(self):
    r = '<'
    for c in self.chars:
      r += str(c)
    r += '>'
    return r
  def __init__(self, fd):
    self.chars = None
    self.value = ''
    
    ###TODO - Anything else we might want? Is this all valid. I think so.
    self.valid_cc = True
    self.valid_initial_cc = True
    
    self.C = False
    self.CC = False
    self.CCC = False
    self.CyC = False
    self.CyCC = False
    self.CCyC = False
    
    self.counts_CC = False
    self.has_C = False
    self.accented = False
    
    self.V = False
    self.VV = False
    self.VhV = False
    self.counts_VV = False
    self.has_V = False
    
    self.h = False
    self.y = False
    self.comma = False
    self.period = False
    self.whitespace = False
    self.wordsep = False
    self.garbage = False
    
    first = fd.pop()
    
    if first.C:
      self.has_C = True
      if fd[0].C:
        ###if fd[1].y and fd[2].C: #CCyC
            ###self.CCyC = True
            ###self.counts_CC = True
            ###self.chars = [first, fd.pop(), fd.pop(), fd.pop()]
        ###el
        if fd[1].C: #CCC or CC CC
          if fd[2].C: #CC CC
            self.CC = True
            self.counts_CC = True
            self.chars = [first, fd.pop()]
          else: #CCC V or something
            self.CCC = True
            self.counts_CC = True
            self.chars = [first, fd.pop(), fd.pop()]
        else: #CC
          self.CC = True
          self.counts_CC = True
          self.chars = [first, fd.pop()]
      elif fd[0].y and fd[1].C and not fd[2].y: #CyC
        #if fd[2].C: 
          #self.CyCC = True
          #self.counts_CC = True
          #self.chars = [first, fd.pop(), fd.pop(), fd.pop()]
        #else:
        self.CyC = True
        self.counts_CC = True
        self.chars = [first, fd.pop(), fd.pop()]
      else:
        self.C = True
        self.chars = [first]
    elif first.V:
      self.has_V = True
      if fd[0].V:
        self.VV = True
        self.counts_VV = True
        self.chars = [first, fd.pop()]
        
      elif fd[0].h and fd[1].V:
        self.VhV = True
        self.counts_VV = True
        self.chars = [first, fd.pop(), fd.pop()]
      else:
        self.V = True
        self.chars = [first]
      #Check for accents
      for letter in self.chars:
        if letter.accented:
          self.accented = True
    else:
      if first.whitespace:
        self.whitespace = True
        self.wordsep = True
        self.chars = [first]
        while fd[0].whitespace:
          self.chars.append(fd.pop())
      elif first.y:
        self.y = True
        self.chars = [first]
        #XXX I don't like this
        #while fd[0].y:
          #self.chars.append(fd.pop())
      elif first.h:
        self.h = True
        self.chars = [first]
      elif first.comma:
        self.comma = True
        self.chars = [first]
      elif first.period:
        self.wordsep = True
        self.period = True
        self.chars = [first]
        while fd[0].period:
          self.chars.append(fd.pop())
      else:
        self.garbage = True
        self.chars = [first]
        while fd[0].garbage:
          self.chars.append(fd.pop())
    
    
    assert self.chars
    self.cc_letter_counts = 0 #How many of this bit's letters count when determining if a CC is within the first 5 letters.
    for char in self.chars:
      self.value += char.value
      if char.V or char.C:
        self.cc_letter_counts += 1
    
    self.position = self.chars[0].position


__VALID_INIT_CC = "bl br cf ck cl cm cn cp cr ct dj dr dz fl fr gl gr jb jd jg jm jv kl kr ml mr pl pr sf sk sl sm sn sp sr st tc tr ts vl vr xl xr zb zd zg zm zv".split(' ')
def valid_init_cc(bit):
  if type(bit) == list:
    assert len(bit) == 2
    assert all(type(x) == str for x in bit)
    return (bit[0]+bit[1]) in __VALID_INIT_CC
  if len(bit.chars) == 4: #CCyC or CyCC
    l, x, z, n = bit.chars
    if x.value == 'y':
      return (z.value+n.value) in __VALID_INIT_CC
    elif z.value == 'y':
      return (l.value+x.value) in __VALID_INIT_CC
    else:
      raise Exception("Miscall with " + str(bit))
    
  elif len(bit.chars) == 3:
    l, m, n = bit.chars
    if l.C and m.y and n.C:
      return True
    elif (l.value+m.value) in __VALID_INIT_CC and (m.value+n.value) in __VALID_INIT_CC:
      return True
    return False
  elif len(bit.chars) == 2:
    m, n = bit.chars
    m, n = m.value, n.value
    v = m+n
    return v in __VALID_INIT_CC
  raise Exception("Miscall with " + str(bit))

if __name__ == '__main__':
  from config import Configuration
  config = Configuration([]) #No. No command arguments for this. 
  
  charbuf = Buffer(stream_char(sys.stdin, config), config)
  bitbuf = Buffer(stream_bit(charbuf), config)
  i = []
  for bit in bitbuf:
    i.append(bit)
    print(repr(bit), end=' ')
  print()