#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
orthography.py - Handle the messy, dirty stuff of input.

This file handles the inputting of text, and the classification and grouping of characters.

TODO: unicodedata.normalize

"""
import sys
import copy

import zirsam.common
import zirsam.config


def clean_val(v):
  #Escapes stuff if neccessary. "\n" -> "\\n"
  if v == '\\': return '\\'
  return repr(v)[1:-1]

class Character:
  __slots__ = "position", "value", "accented", "V", "C", "y", "comma", "period", "h", "whitespace", "garbage", "EOF", 
  def __str__(self):
    return clean_val(self.value)
  
  def __repr__(self):
    #return "{0}={1}".format(self, self.value)
    #return "<{0} {1}>".format(self.value, self.position)
    return str(self)
  
  def __init__(self, c, konf):
    """
    A single character.
    ``c'' is that character, ``konf'' is the zirsam.config.Configuration object that holds the current position.
    """
    #self.original = c
    
    self.position = zirsam.common.Position(konf.position)
    self.value = c
    
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
    
    if c == '':
      self.EOF = True
    elif c in 'AEIOU':
      self.accented = True
      self.V = True
    elif c in 'aeiou':
      self.V = True
    elif c in "bcdfgjklmnprstvxz":
      self.C = True
    elif c in 'y':
      self.y = True
    elif c in ',': 
      self.comma = True
    elif c in '.':
      self.period = True
    elif c in "'":
      self.h = True
    elif c in ' \t\n\r': #Could be put into config or something
      self.whitespace = True
    else:
      self.garbage = True
    


class Bit:
  """Stores a logical sequence of characters
  XXX A better name? Cluster
  """
  def __str__(self):
    r = ''
    for c in self.chars:
      r += c.value
    return r
  
  def __repr__(self):
    r = '<'
    for c in self.chars:
      r += str(c)
    r += '>'
    return r
  
  def __len__(self):
    return len(self.chars)
  
  def __getitem__(self, index):
    return self.chars[index]
  __slots__ = "chars", "value", "valid_cc", "valid_initial_cc", "C", "CC", "CCC", "CyC", "CyCC", "CCyC", "counts_CC", "has_C", "V", "VV", "VhV", "counts_VV", "has_V", "accented", "h", "y", "comma", "period", "whitespace", "wordsep", "garbage", "cc_letter_counts", "position"
  def __init__(self, fd):
    """
    Create a group of characters
    """
    self.chars = None
    self.value = ''
    
    self.valid_cc = True
    self.valid_initial_cc = True
    
    self.C = False
    self.CC = False
    self.CCC = False
    self.CyC = False
    self.CyCC = False
    self.CCyC = False # XXX - CCyC and CyCC counts as CCC, right?
    
    self.counts_CC = False
    self.has_C = False
    
    self.V = False
    self.VV = False
    self.VhV = False
    self.counts_VV = False
    self.has_V = False
    self.accented = False
    
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
    elif first.whitespace:
      self.whitespace = True
      self.wordsep = True
      self.chars = [first]
    elif first.y:
      self.y = True
      self.chars = [first]
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
  
  
  #def __bool__(self): raise Exception("No")

__VALID_INIT_CC = "bl br cf ck cl cm cn cp cr ct dj dr dz fl fr gl gr jb jd jg jm jv kl kr ml mr pl pr sf sk sl sm sn sp sr st tc tr ts vl vr xl xr zb zd zg zm zv".split(' ')
def valid_init_cc(bit):
  if type(bit) in (list, str):
    #assert len(bit) == 2
    #assert all(type(x) == str for x in bit)
    return (bit[0]+bit[1]) in __VALID_INIT_CC
  if len(bit.chars) == 4: #CCyC or CyCC
    l, x, z, n = bit.chars
    if x.value == 'y':
      return (z.value+n.value) in __VALID_INIT_CC
    elif z.value == 'y':
      return (l.value+x.value) in __VALID_INIT_CC
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

class __NiceStdin:
  #Use the input() function to get data; this allows the use of GNU readline to edit the text
  def __init__(self):
    self.chars = ''
  def isatty(self):
    return False
  def read(self, i=1):
    if len(self.chars) == 0:
      if 1: #not self.EOF or 1:
        try:
          l = input() + '\n' #input() strips the newline
        except EOFError:
          l = ''
        self.chars += l
      else:
        return ''
    x = self.chars[:i]
    self.chars = self.chars[i:]
    return x
    

def stream_char(config):

  while 1:
    #c = fd.read(1)
    #This is where we do that GlyphTable stuff
    c = config.glyph_table.get_char(config)
    #assert c.lower() in "bcdfgjklmnprstvxz \n ',. aeiouy"

    if c == []:
      #XXX I don't think that stuff below is needed anymore; but if I find errors...
      #yield Character('\n', config) # haXXX, if morphology doesn't get a whitespace at the end it doesn't give up the last token
      #yield Character('', config) #XXX ? I don't need anymore?!?
      break
    else:
      for _c in c:
        yield _c
        #yield Character(_c, config)

def stream_bit(fd):
  while 1:
    if fd.EOF:
      break
    yield Bit(fd)

def Stream(conf=None):
  if conf == None:
    conf = zirsam.config.Configuration()
  
  
  if conf.stdin.isatty():
    if conf.permit_readline: #Should we enable GNU readline?
      try:
        import readline
        #If this succeeds, then it is enabled for the input() function
        conf.stdin = __NiceStdin()
      except ImportError:
        pass
    elif conf.cbreak:
      raise Exception("--cbreak not implemented.")
      ##import curses
      ##scr = curses.initscr()
      
      ###Mess up terminal
      ###import tty
      ###tty.cbreak(1)
      ###print('raw')
      ###import sys, tty, termios
      ###fd = sys.stdin.fileno()
      ###old_settings = termios.tcgetattr(fd)
      ###tty.setraw(sys.stdin.fileno())
      ###import atexit
      ###atexit.register(termios.tcsetattr, fd, termios.TCSADRAIN, old_settings)
      ####tty.setraw(1)
  charbuf = zirsam.common.Buffer(stream_char(conf), conf)
  bitbuf = zirsam.common.Buffer(stream_bit(charbuf), conf)
  return bitbuf

if __name__ == '__main__':
  #print("Shows the grouping of letter clusters", file=sys.stderr)
  bitbuf = Stream()
  r = []
  for bit in bitbuf:
    r.append(bit)
    if bitbuf.config._debug:
      print(bit.position, ": ", repr(bit), sep='')
    else:
      print(repr(bit), end='')
  print()
