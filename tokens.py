# -*- coding: utf-8 -*-

#Different kinds of tokens
import io

import config
import common
import orthography

from selmaho import SELMAHO


class Token:
  #The items below are a hack for the morphology module, which re-inserts tokens into the Bit stream.
  #With these values, nobody will try to re-tokenize it.
  wordsep = True
  h = False
  y = False
  counts_CC = False
  has_V = False
  def __init__(self, bits, config):
    self.config = config
    self.bits = bits
    if not len(bits):
      self.config.error("Trying to tokenize nothing!")
    self.position = self.bits[0].position
    self.value = self.calculate_value()
    self.type = ...
    self.ve_lujvo_rafsi = []
    self.classify()
    self.content = None
    self.modifiers = [] #BAhE and UI such.
    self.whitespace = [] #Whitespace and pauses that occur BEFORE the token.
    self.end = None #Acceptable types: None, Token
    if self.config.hate_token and self.config.hate_token == self.value:
      #Be hatin' - for morphology debugging
      raise Exception("Tokenization Backtrace")

  def classify(self):
    #Sets self.type to whatever is appropriate
    #Also verifies lujvo/fu'ivla
    if self.type != ...:
      return
    if isinstance(self, CMAVO):
      #All cmavo should have a value!
      self.value = self.value.lower()
      if self.value in SELMAHO:
        self.type = SELMAHO[self.value]
      else:
        self.config.warn("Unknown cmavo %r"%(self.value), self.position)
        self.type = SELMAHO['CIZMAhO']
    elif isinstance(self, SELBRI):
      #A gismu, a lujvo, or a fuhivla?
      #gismu: CCVCV or CVCCV
      #This will probably never be used.
      if len(self.bits) == 4:
        if self.bits[0].CC and self.bits[1].V and self.bits[2].C and self.bits[3].V:
          self.type = GISMU
        elif self.bits[0].C and self.bits[1].V and self.bits[2].CC and self.bits[3].V:
          self.type = GISMU
        else:
          if self._lujvo_analyze(self.value):
            self.type = LUJVO
            #Like "klakla"
          else:
            self.type = FUHIVLA
            
          
      else:
        if self._lujvo_analyze(self.value):
          self.type = LUJVO
        else:
          self.type = FUHIVLA
    else:
      #cmene, or possibly pre-defined (as lujvo/gismu/fuhivla), or maybe garbage
      #fu'ivla need to pass the slinku'i test, however, fu'ivla from {2.C.4)b)5]e]3>} (which are the only source of pre-defined fu'ivla) are pretty much defined as passing slinku'i I think XXX
      t = type(self)
      if t == Token:
        raise Exception("No type for Token")
      
      self.type = t

    if self.type == FUHIVLA:
      self._test_slinkuhi()

  def __eq__(self, other):
    return isinstance(other, Token) and (self.type == other.type) and (self.value == other.value)
  def _test_slinkuhi(self):
    test_word = 'pa'
    test = test_word+self.value
    #See if it matches a lujvo...
    #hackish, REALLY NEED to do something better with lujvo analyzation stuff...
    orig_ve_lujvo_rafsi = self.ve_lujvo_rafsi
    if self._lujvo_analyze(test):
      self.config.warn("This ambigious fu'ivla fails the slinku'i test (\"{0}\" is a lujvo, not \"{1} {2}\")".format(test, test_word, self.value), self.position)

  def _match_form(self, chars, form, is_first):
    i = 0
    rafsi = ''
    while i != len(form):
      f = form[i]
      try:
        c = chars[i]
      except:
        return False
      if f == 'y' and not c.y: return False
      if f == 'C' and not c.C: return False
      if f == 'V' and not c.V: return False
      if f == 'h' and not c.h: return False
      if f == '|' and not c.whitespace: return False
      if f == '-': #a hyphen letter; r or n
        if (is_first and c.value in 'rn'):
          if c.value == 'n' and chars[i+1].value != 'r': #xorxes says n must be followed by r
            return False
        else:
          return False
        
      
      rafsi += str(chars[i])
      i += 1
    return rafsi
  def _add_rafsi(self, chars, i):
    #Semi-hackish: remove y
    rafsi = ''
    while i > 0:
      c = chars.pop(0)
      rafsi = rafsi + c.value
      i -= 1
    if rafsi[-1] == 'y':
      y = 'y'
      rafsi = rafsi[:-1]
    else:
      y = None
    self.ve_lujvo_rafsi.append(rafsi)
    if y:
      self.ve_lujvo_rafsi.append(y)
    return chars

  def _lujvo_analyze(self, value):
    #XXX TODO Not everything that isn't a gismu/lujvo/cmavo is a fu'ivla
    #XXX Move somewhere else?
    self.ve_lujvo_rafsi = []
    chars = list(orthography.stream_char(config.Configuration(stdin=io.StringIO(value+' '), args=[]))) #XXX why you need that extra space, eh?
    orig_chars = list(chars)
    forms = [0]
    
    def next_form():
      #The current item didn't work, so pick the next.
      if forms[-1] > len(all_):
        #Out of items here...
        forms.pop()
      if forms == []:
        return True #FUHI!
      forms[-1] += 1
      return False
    len_form = lambda: sum(len(all_[_]) for _ in forms[:-1])
    
    ##http://www.lojban.org/sv/lists/lojban-list/msg16628.html
    terminal_rafsi = "CCV| CVV| CVhV| CVCCV| CCVCV|".split(' ')
    rafsi4 = "CVCCy CCVCy".split(' ')
    rafsi3 = "CVV- CVhV- CVC CVCy CVV CVhV CCV".split(' ')
    all_ = terminal_rafsi + rafsi4 + rafsi3
    
    
    while 1:
      len_ = len_form()
      chars = orig_chars[len_:]
      if chars == []:
        break
      
      try:
        test = self._match_form(orig_chars[len_:], all_[forms[-1]], len(forms) == 1)
      except Exception as e:
        test = False
      #len_ = len_form()
      
      if test:
        #chars = test
        if all_[forms[-1]][-1] == '|':
          break
        forms.append(0)
      else:
        if next_form():
          return False #Ran out of checks. FUHI!
      
    #You think you found a lujvo
    #XXX: Do I need to check for doubling?
    first = all_[forms[0]]
    if first in ["CVV", "CVhV"]:
      #xorxes says a CVV must end with CCV.
      if len(forms) != 2 or all_[forms[1]] != "CCV|":
        return False
    #"Check the consonant that follows CVC or CVCy." - I trust he refers to the following paragraph? >_>
    #Maybe consonant clusters?
    i = 0
    for form in forms:
      if all_[form][:2] == 'CC':
        #Check consonant clusters
        if not orthography.valid_init_cc(orig_chars[i].value+orig_chars[i+1].value):
          self.config.debug("Invalid consonant cluster for lujvo: {0}".format(self)) #XXX - config.warn
          return False
      i += len(all_[form])
    '''
    if first in ['CVC', 'CVCy']:
      if not self._lujvo_analyze(value[2:]):
        return False
    '''
    
    while forms:
      _ = all_[forms.pop(0)]
      orig_chars = self._add_rafsi(orig_chars, len(_))
    #remove hyphen-letter
    
    if first in ["CVV-," "CVhV-"]:
      #Remove the hyphen
      self.ve_lujvo_rafsi[0] = self.ve_lujvo_rafsi[0][:-1]
    
    self.ve_lujvo_rafsi[-1] = self.ve_lujvo_rafsi[-1][:-1] #Dump the whitespace from the begining
    return True

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
    if self.ve_lujvo_rafsi:
      val += '=' + '+'.join(self.ve_lujvo_rafsi)
    r = "{0}({1})".format(self.__getname(), val)
    if self.modifiers:
      for _ in self.modifiers:
        r += '_'+str(_)

    return r

  def calculate_value(self):
    """
    Return the ascii value of the token
    XXX This feels out of place
    """
    #Assemble a string out of the values of every bit
    v = ''
    bad_bit = False
    for bit in self.bits:
      v += bit.value
      if not isinstance(bit, orthography.Bit):
        bad_bit = True

    if bad_bit:
      ##self.config.warn("Observation: A token of non-bits has been made, so it might have a weird value", self.bits[0].position)
      ##self.config.debug(repr(self.bits)+'='+v, self.bits[0].position)
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


class VALSI(Token): pass
class   CMENE(VALSI): pass
class   CMAVO(VALSI): pass
class   SELBRI(VALSI): pass
class     GISMU(SELBRI): pass
class     LUJVO(SELBRI): pass
class     FUHIVLA(SELBRI): pass
class     CIZYSELBRI(SELBRI): pass
BRIVLA = SELBRI #I prefer SELBRI, lojban.bnf uses BRIVLA  XXX could replace it in the BNF


class EXTRA(Token): pass #Something that can't be parsed
class   GARBAGE(EXTRA): pass #Strange characters in Lojbanistan
class   NONLOJBAN(EXTRA): pass #Contents of a zoi-quote


class IGNORABLE(Token): pass #Not needed in grammer parsing
class BORING(Token): pass #tokens don't uffect parsing; clients that do text transformation might want them
class   WHITESPACE(BORING, IGNORABLE): pass
class   PERIOD(BORING, IGNORABLE): pass
class   HESITATION(BORING): pass #Should be absorbed into (sigh) the previous token
class   DELETED(BORING, IGNORABLE): pass #Nothing uses this

