# -*- coding: utf-8 -*-

#Different kinds of tokens

import orthography
from selmaho import SELMAHO


class Token:
  #The items below are a hack for the morphology module, which re-inserts tokens into the Bit stream.
  #With these values, nobody will try to re-tokenize it.
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
    '''
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
    '''

  def __str__(self):
    val = str(self.value)
    if self.content:
      val += ', content=' + str(self.content)
    if self.end:
      val += ', end=' + str(self.end)
    r = "{0}({1})".format(self.__getname(), val)
    if self.modifiers:
      for _ in self.modifiers:
        r += '_'+str(_)
    return r

  def calculate_value(self, config):
    """
    Return the ascii value of the token
    TODO This feels out of place here.
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
    self.ve_lujvo_rafsi = []
    self.classify(config)
    self.content = None
    self.modifiers = [] #Emphasis and such.
    self.end = None #Acceptable types: None, Token
    if config.hate_token and config.hate_token == self.value:
      #Be hatin' - for morphology debugging
      raise Exception("Tokenization Backtrace")

  def classify(self, config):
    if self.type != ...:
      return
    if isinstance(self, CMAVO):
      #All cmavo should have a value
      self.value = self.value.lower()
      if self.value in SELMAHO:
        self.type = SELMAHO[self.value]
      else:
        config.warn("Unknown cmavo %r"%(self.value), self.position)
        self.type = SELMAHO['CIZMAhO']
    elif isinstance(self, SELBRI):
      #A gismu, a lujvo, or a fuhivla?
      #gismu: CCVCV or CVCCV
      #XXX TODO: Detect lujvo/fu'ivla forms
      if len(self.bits) == 4:
        if self.bits[0].CC and self.bits[1].V and self.bits[2].C and self.bits[3].V:
          self.type = GISMU
        elif self.bits[0].C and self.bits[1].V and self.bits[2].CC and self.bits[3].V:
          self.type = GISMU
        else:
          if self._lujvo_analyze():
            self.type = LUJVO
          else:
            self.type = FUHIVLA
          #raise Exception("Now what?")
      else:
        if self._lujvo_analyze():
          self.type = LUJVO
        else:
          self.type = FUHIVLA
    else:
      #cmene, or possibly pre-defined (as lujvo/gismu/fuhivla), or maybe garbage
      self.type = type(self)

  def _ccc2cc_c(self, i):
    print(self.bits)
    base = self.bits.pop(i)
    import sys
    sys.b = base
    head, *tail = base.split(1)
    while tail:
      self.bits.insert(i, tail.pop())
    self.bits.insert(i, head)
    print("Turned", base, "into", head, "and", tail)
    print(self.bits)
    return head, tail
  def _get_lujvo_part(self, s=0):
    #Rafsi forms: CVCCV, CCVCV, CVCC, CCVC, CCV, CVC, CVV
    #Items that end in C/CC may need to be split
    l = len(self.bits)
    class Foo:
      class Bar:
        def __init__(self): self.y = self.V = self.C = self.CC = self.CCC = self.has_C = self.counts_V = self.counts_C = False
      def __init__(self, bits): self.bits = bits
      def __getitem__(self, i):
        if i >= l: return Foo.Bar()
        b = self.bits[i]
        #if b.CyC: return Foo.Bar()
        return b
    
    test = Foo(self.bits)
    if test[s].y:
      return 1 #y
    elif test[s].C:
      if test[s+1].counts_VV: #CVV
        if s == 0: #Check hyphen words
          if test[s+2].value[0] in 'rn':
            if not test[s+2].C:
              self._ccc2cc_c(s+2)
            return 3
        return 2
      elif test[s+1].V:
        if test[s+2].CC or test[s+2].CCC:
          if test[s+2].CCC:
            self._ccc2cc_c(s+2)
            
          if test[s+3].V: #CVCCV
            return 4
          else:
            return 3 #CVCC
        elif test[s+2].has_C:
          if not test[s+2].C:
            self._ccc2cc_c(s+2) #CVC (C...)
          return 3 #CVC
    elif test[s].CC and test[s+1].V:
      if test[s+2].has_C:
        if test[s+3].V: #CCVCV
          return 4
        else:
          if (not test[s+2].C) and (test[s+2].has_C): #CCVC...
            self._ccc2cc_c(s+2)
          return 3 #CCVC
      else:
        return 2 #CCV

  def _lujvo_analyze(self):
    #Are we lujvo, or fuhivla?
    #self.ve_lujvo_rafsi = []
    s = 0
    while 1:
      i = self._get_lujvo_part(s)
      print(i)
      if i: # and i != s:
        self.ve_lujvo_rafsi.append(self.bits[s:s+i])
        print(self.bits[s:s+i])
        s += i
        
      else:
        break
    if s == len(self.bits):
      print(">>>", self.bits)
      print(">>>", self.ve_lujvo_rafsi)
      
      return True
      #self.type = LUJVO
    else:
      print("Not lujvo.")
      print(self.ve_lujvo_rafsi)
      self.ve_lujvo_rafsi = []



class VALSI(Token): pass
class   CMENE(VALSI): pass
class   CMAVO(VALSI): pass
class   SELBRI(VALSI): pass
class     GISMU(SELBRI): pass
class     LUJVO(SELBRI): pass
class     FUHIVLA(SELBRI): pass
BRIVLA = SELBRI #I prefer SELBRI, lojban.bnf uses BRIVLA  XXX could replace it in the BNF


class EXTRA(Token): pass #Something that can't be parsed
class   GARBAGE(EXTRA): pass #Strange characters in Lojbanistan
class   NONLOJBAN(EXTRA): pass #Contents of a zoi-quote


class IGNORABLE(Token): pass #Not needed in grammer parsing
class BORING(Token): pass #tokens don't uffect parsing; clients that do text transformation might want them
class   WHITESPACE(BORING, IGNORABLE): pass
class   PERIOD(BORING, IGNORABLE): pass
class   HESITATION(BORING): pass #Should be absorbed into (sigh) the previous token
class   DELETED(BORING, IGNORABLE): pass #Not used

