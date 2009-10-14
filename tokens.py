# -*- coding: utf-8 -*-

#Different kinds of tokens


from selmaho import SELMAHO

class Token:
  #The items below are a hack for the morphology module. With these values, nobody will try to re-tokenize it.
  wordsep = True
  h = False
  y = False
  counts_CC = False

  def __repr__(self):
    r = type(self).__name__+'('
    for i in self.bits:
      r += repr(i)
    return r+repr(self.bits[0].position)+')'

  def __str__(self):
    #r = ''
    #for b in self.bits:
      #r += str(b)
    return "{0}({1})".format(type(self).__name__, self.value)

  def calculate_value(self):
    """
    Return the ascii value of the token
    """
    #Assemble a string out of the values of every bit
    v = ''
    for bit in self.bits:
      v += bit.value
    #Check for irregular stress. If the stress is regular, then we can do str.lower()
    #We want penultimate stress.
    stressed_regularly = ...
    i = len(self.bits)
    encountered_vowels = 0
    while i >= 0:
      i -= 1
      if self.bits[i].has_V:
        encountered_vowels += 1
      if self.bits[i].accented and encountered_vowels != 2:
        stressed_regularly = False

    if stressed_regularly:
      return v.lower() #Eliminates unecessary accents
    return v #Keep the given accents

  def __init__(self, bits, config):
    self.bits = bits
    if not len(bits):
      config.error("Trying to tokenize nothing!")
    self.position = self.bits[0].position
    self.value = self.calculate_value()
    self.type = ...
    self.classify()
    if config.hate_token and config.hate_token == self.value:
      #Be hatin'
      raise Exception("Tokenization Backtrace")

  def classify(self):
    if self.type != ...:
      return
    if isinstance(self, CMAVO):
      #All cmavo should have a value
      self.type = SELMAHO[self.value]
    elif isinstance(self, SELBRI):
      #A gismu, a lujvo, or a fuhivla?
      #gismu: CCVCV or CVCCV
      if self.bits[0].CC and self.bits[1].V and self.bits[2].C and self.bits[3].V:
        self.type = GISMU
      elif self.bits[0].C and self.bits[1].V and self.bits[2].CC and self.bits[3].V:
        self.type = GISMU
      else:
        raise Exception("TODO: Detect lujvo/fu'ivla forms!") #XXX
    else:
      #cmene, or possibly instantiated as a lujvo/gismu/fuhivla, or maybe garbage
      self.type = type(self)


class VALSI(Token): pass

class CMENE(VALSI): pass
class CMAVO(VALSI): pass
class SELBRI(VALSI): pass
class GISMU(SELBRI): pass
class LUJVO(SELBRI): pass
class FUHIVLA(SELBRI): pass

class BORING(Token): pass #Don't mention these items. BORING is a fake token
class WHITESPACE(BORING): pass


class EXTRA(Token): pass #
class GARBAGE(EXTRA): pass
class PERIOD(EXTRA, BORING): pass
class HESITATION(EXTRA): pass
