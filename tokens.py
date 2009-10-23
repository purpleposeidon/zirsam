# -*- coding: utf-8 -*-

#Different kinds of tokens

import orthography #Amusingly enough, modules can recursively import eachother
from selmaho import SELMAHO

class Token:
  #The items below are a hack for the morphology module. With these values, nobody will try to re-tokenize it.
  wordsep = True
  h = False
  y = False
  counts_CC = False

  def __getname(self):
    if self.type == ...:
      return type(self).__name__
    else:
      return self.type.__name__

  def __repr__(self):
    return str(self)
    #The below is more informative, but fugly
    r = self.__getname()+'('
    for i in self.bits:
      r += repr(i)
    end = ''
    if self.content:
      end += ', content=' + repr(self.content)
    if self.end:
      end += ', end=' + repr(self.end)
    return r+repr(self.bits[0].position)+end+')'

  def __str__(self):
    val = str(self.value)
    if self.content:
      val += ', content=' + str(self.content)
    if self.end:
      val += ', end=' + str(self.end)
    return "{0}({1})".format(self.__getname(), val)

  def calculate_value(self, config):
    """
    Return the ascii value of the token
    """
    #Assemble a string out of the values of every bit
    v = ''
    bad_bit = False
    for bit in self.bits:
      v += bit.value
      if not isinstance(bit, orthography.Bit):
        bad_bit = True

    if bad_bit:
      ##config.warn("Observation: A token of non-bits has been made, so it might have a weird value", self.bits[0].position)
      ##config.debug(repr(self.bits)+'='+v, self.bits[0].position)
      return v
      
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
    self.value = self.calculate_value(config)
    self.type = ...
    self.classify(config)
    self.content = None
    self.end = None
    if config.hate_token and config.hate_token == self.value:
      #Be hatin'
      raise Exception("Tokenization Backtrace")

  def classify(self, config):
    if self.type != ...:
      return
    if isinstance(self, CMAVO):
      #All cmavo should have a value
      if self.value in SELMAHO:
        self.type = SELMAHO[self.value]
      else:
        config.warn("Unknown cmavo %r"%(self.value), self.position)
        self.type = SELMAHO['UNKNOWN']
    elif isinstance(self, SELBRI):
      #A gismu, a lujvo, or a fuhivla?
      #gismu: CCVCV or CVCCV
      #XXX Todo: Detect lujvo/fu'ivla forms
      if len(self.bits) == 4:
        if self.bits[0].CC and self.bits[1].V and self.bits[2].C and self.bits[3].V:
          self.type = GISMU
        elif self.bits[0].C and self.bits[1].V and self.bits[2].CC and self.bits[3].V:
          self.type = GISMU
        else:
          self.type = SELBRI
          #raise Exception("How what?")
      else:
        self.type = SELBRI
    else:
      #cmene, or possibly instantiated as a lujvo/gismu/fuhivla, or maybe garbage
      self.type = type(self)



class VALSI(Token): pass
class   CMENE(VALSI): pass
class   CMAVO(VALSI): pass
class   SELBRI(VALSI): pass
class     GISMU(SELBRI): pass
class     LUJVO(SELBRI): pass
class     FUHIVLA(SELBRI): pass
BRIVLA = SELBRI #I prefer SELBRI, lojban.bnf uses BRIVLA  XXX could replace it in the BNF


class EXTRA(Token): pass #Something that can't be parsed
class   GARBAGE(EXTRA): pass
class   NONLOJBAN(EXTRA): pass


class BORING(Token): pass #tokens don't uffect meaning; lower-level clients might want access to them tho
class   WHITESPACE(BORING): pass
class   PERIOD(BORING): pass
class   HESITATION(BORING): pass
class   DELETED(BORING): pass

