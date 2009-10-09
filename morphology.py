#!/usr/bin/python3.0
# -*- coding: utf-8 -*-

__version__ = "0" #I expect it will only get worst
__author__ = "djeims.roistn <purpleposeidon@gmail.com>"

"""

"""

import io
import sys
import inspect

from common import Buffer
import orthography
from orthography import valid_init_cc
from config import Configuration
from tokens import *

"""
Desired cl options:
  Input Options
    STRICT - Pure lojban
    MIXED - Hunt down lojban text in otherwise {english text}?
    AUTOQUOTE - Automatic quote of obviously foreign texts? For example, chinese text.
    DECOMPRESS - Input lojban is pre-parsed morphological symbols
    
  Parsing Options
    NOWARN - Don't warn about usage errors
    DOTSIDE - Require names to be dotsid'd
    NOSU - Speed up parsing by not needing to cache the entire text?
    NOSI - Kinda like NOSU. But only caches 2 sentances.
    BADGARBAGE - error on garbage
    EXTENDED - Include (experimental) language extensions
    THREADING - Make each level of abstraction a different thead...?
    DICTD - Use lojban's dictd/jbovlaste to look up/validate words
    
  Output Options
    NORMALIZE - Output normalized lojban (Elided terminators, space-sep words, zo'e instead of SE/FA)
    REPAIR - Fix errors
    1337 - Output 31337 lojban
    SMOOSH - No spaces
    GRAVE - Use fancy accent marks in output
    TRANSLATE - attempt translation
    STRUCTURE - show strucutre
    INTEPRET - Substitute out pro-sumti
    UNTANGLE - Convert fa sumti se xe te broda fi ma to, uh, whatever that would be
    COMPRESS - Compress text using my compression idea
  
  Warning options:
    Cultural items
    Invalid use of la/doi/etc in cmene
    Cmene that aren't dotside
  
"""



#TODO: Single characters that expand to multiple characters
#Also: diaerisies. I think, also + - / *, =?
{'1':'pa', '2':'re', '3':'ci', '4':'vo', '5':'mu', '6':'xa', '7':'ze', '8':'bi', '9':'so', '0':'no'}

class ParsingError(Exception): pass #For when your input sucks
class InternalError(Exception): pass #For when your program sucks


def lineno():
    #Returns the current line number in our program. Debug thing.
    return inspect.currentframe().f_back.f_lineno








#The 4 items below are utility functions used in ValsiParser.break_a_selbri. They deal with the endgame.
lentest = lambda lets, N: len(lets) - 1 >= N

def match(lets, pos, values):
  #Does letters[pos] match the form given by values?
  if len(lets[pos:]) < len(values):
    return False
  for v in values:
    if v == 'C':
      if not lets[pos].C: return False
    elif v == 'V':
      if not lets[pos].V: return False
    elif v in "h'":
      if not lets[pos].h: return False
    else:
      raise Exception("Invalid match string %r" % values)
    pos += 1
  return True

def matchall(lets, pos, values):
  #Does len(letters) == len(values) and does it match?
  if len(values) == len(lets[pos:]):
    return match(lets, pos, values)
    
  
def test(lets, pos, forms, match_function):
  #Look for a matching form. Returns the number of items in that form. If not, then it returns None
  rs = []
  
  for form in forms:
    
    if match_function(lets, pos, form):
      rs += [len(form)]
      return len(form)
  if rs:
    return max(rs)
    
  


class ValsiParser:
  def __init__(self, bit_iter, config):
    """
    djeims' valsi parser. It should and ought to follow the algorithm specified in docs/BRKWORDS.TXT
    """
    self.bit = bit_iter
    self.config = config
  
  def __iter__(self):
    while 1:
      try:
        v = self.get_token()
      except EOFError:
        self.config.debug("EOF hit in ValsiParser")
        return
      if v == ...:
        continue
      elif v == None or v == []:
        break
      elif type(v) in (list, tuple):
        for extra_token in v:
          yield extra_token
      else:
        yield v
  
  #Utilities for ValsiParser.bit
  def word(self, start=0):
    #Returns the number of bits that are part of the word
    i = start
    try:
      while not self.bit[i].wordsep:
        i += 1
    except EOFError:
      self.config.debug("EOF touched in word()", self.bit[i].position)
      return i
    return i
  
  def locate_cc(self, start=0):
    #Return (Bit index of a CC or CyC, number of non-h letters)
    #Bit Index is indexed from 0, Non-h letters starts at 1.
    letter_count = 0
    while 1:
      try:
        cur = self.bit[start]
      except EOFError:
        self.debug("EOFError hit in locate_cc", self.bit[0].position)
        raise EOFError
      if cur.wordsep: #Errors? This used to be below the for
        return -1, letter_count+1
      
      if cur.counts_CC:
        return start, letter_count+1
      for c in cur.chars:
        if not c.h:
          letter_count += 1
      
      start += 1
    raise Exception()
  
  def locate_ps(self, start):
    #{2.C.2)} - Return the index of the penultimate stress
    if start >= 1 and self.bit[start-1].accented:
      #{2.C.2)a)} and {2.C.2)b)} are taken care of by orthography.py, as diphthongs are kept together
      #a) is part because the selbri (or cmavo+selbri) always starts at 0 because everything in front
      #   has been broken off alerady
      #b) is satisfied because dipthongs are handled together
      return start - 1
    locus_ps = start
    
    #{2.C.2)c)}
    found_word_end = False
    while 1:
      locus_ps += 1
      #self.config.debug(self.bit[locus_ps], repr(locus_ps), self.bit[locus_ps].accented)
      if self.bit[locus_ps].wordsep:
        found_word_end = True
        locus_ps -= 1 #XXX Test it, see {obupykyburysyty.ubuvyvybuxy.ybuzy}
        break
      elif self.bit[locus_ps].accented:
        return locus_ps

    
    if found_word_end:
      #Uh, okay. So, we're like... lujvolujvoluvjo@
      #Step back two vowels.
      vowel_count = 0
      while locus_ps >= 0:
        #print("info:", self.bit[locus_ps])
        if self.bit[locus_ps].has_V:
          vowel_count += 1
          if vowel_count == 2:
            return locus_ps
        locus_ps -= 1
    return False
    
  
  def tokenize(self, count, t_type, start=0):
    #Pops count letters (1-indexed) from ValsiParser.bit, and creates a Token object (as given by t_type). The token is returned.
    #If --token-error is given as a config value, it will raise an error.
    v = []
    assert count > 0
    assert start >= 0
    while count:
      b = self.bit.pop(start)
      if len(v) and b.wordsep:
        m = "\n\t".join(['\tConsumed Letters: '+str(v), 'Failed letter: '+repr(b), 'Bit Buffer: '+str(self.bit.buffer)])
        self.config.debug('EXCEPTION INFO:\n'+m)
          
        raise Exception("Tokenizing more than one word")
      v.append(b)
      count -= 1
    the_token = t_type(v, self.config)
    if self.config.token_error or self.config.print_tokens:
      self.config.message("TOKEN {0} {1}".format(t_type.__name__, v))
    if self.config.token_error:
      raise Exception("Token Call Backtrace")
    
    if t_type == GARBAGE:
      self.config.strict("Garbage token: {0}".format(v), v[0].position)
    return the_token
  
  
  
  def break_a_selbri(self):
    """This function is called when a CC is in the text. It deals with the notable issue of seperating selbri and cmavo. It returns either a single token, or a list of tokens. Should all fail, it will make the word a garbage token
    TODO : Include brkword's error detections
    TODO : Look at all the pretty self.tokenize's
    """
    #{2.C.}
    
    #Load up on positions
    
    cc, cc_location = self.locate_cc()
    ps = self.locate_ps(cc)
    word_end = self.word() #This is indexed from 1
    
    self.config.debug("""BUFFER: {0}
cc_location: {1}
cc: {2}
PS: {3}
we: {4}""".format(self.bit.buffer, cc_location, cc, ps, word_end))
    
    
    
    letters = [] #This is used for some form-checking
    for bit in self.bit.items(word_end):
      if bit.wordsep:
        break
      for char in bit.chars:
        letters.append(char)
    
    #{2.C.1)} - error checking
    
    if ps == False and cc == -1:
      #{2.C.1)a)} - cc but no ps
      self.config.warn("Has a consonant cluster, but no penultimate stress", self.bit[0].position)
      return self.tokenize(word_end, GARBAGE)
    #{2.C.1)b)} is taken care of in get_token()
    
    
    #{2.C.3)}
    #Locate the end of the brivla
    end_of_brivla = ps
    alter_PS = False
    found_v = False
    
    END_WORD = False
    
    while 1:
      end_of_brivla += 1 #First time, we move off of the vowel
      
      try:
        bit = self.bit[end_of_brivla]
        if bit.wordsep:
          END_WORD = True
      except EOFError:
        self.config.debug("EOF hit in break_a_selbri()")
        END_WORD = True
      
      if END_WORD:
        end_of_brivla -= 1
        if not found_v:
          #part of {2.C.3)b)} - it is required to have a vowel!
          self.config.warn("This supposed selbri is supposed to have a vowel", self.bit.buffer[0].position)
          return self.tokenize(end_of_brivla, GARBAGE)
        break #There's the end. Stops the while loop
      if bit.has_V:
        found_v = True
        break

    #{2.C.3)c)} - end_of_brivla has now been set to the true end. 
    
    self.config.debug("eb: {0}".format(end_of_brivla))
    
    #{2.C.4)} - Now begins the epic journey to the begining
    
    
    init_cmavo_tokens = []
    
    #{2.C.4)a)]} - break off begining cmavo pieces, like {lonudoklama}
    while cc_location >= 5:
      #{2.C.4)a)1]} and {2.C.4)a)2]}
      #cc is the LETER position of the con cluster, not the actual loccccatttioonn..
      if self.bit[0].has_V:
        
        init_cmavo_tokens.append(self.tokenize(1, CMAVO))
      elif self.bit[0].has_C:
        init_cmavo_tokens.append(self.tokenize(2, CMAVO))
      else:
        break
      cc, cc_location = self.locate_cc()
    if init_cmavo_tokens:
      return init_cmavo_tokens
    
    #self.config.debug(has_starting_cc)
    
    
    #{2.C.4)a)3]}
    if letters[0].V:
      find_first_consonant = 0
      for bit in self.bit:
        if bit.has_C:
          break
        if bit.whitespace:
          break
        find_first_consonant += 1
      
      
      if self.bit[find_first_consonant].counts_CC:
        return self.tokenize(word_end, SELBRI)
      else:
        return self.tokenize(find_first_consonant, CMAVO)
      
    else:
      #{2.C.4)b)} - it starts with a consonant. And should have a CC by this point
      #Things are really get cracking now!
      #self.config.debug(self.bit.buffer)
      if self.bit[0].counts_CC or  (self.bit[0].C and self.bit[1].V and self.bit[2].CyC) : #CC... CVCyC...
        #{2.C.4)b)1]} - more selbri should be like this
        #Except, I want to implement more error checking!
        for bit in self.bit.items(end_of_brivla+1):
          if bit.garbage:
            self.config.warn("This supposed selbri has garbage in it", bit.position)
        return self.tokenize(end_of_brivla+1, SELBRI)
      elif self.bit[0].CyC:
        #{2.C.4)b)2]} - I'm not sure this is neccessary. Why is this neccessary?
        # Would it not be handled with everything else?
        return self.tokenize(word_end, GARBAGE)
      elif self.bit[0].C and self.bit[1].counts_VV and (self.bit[2].CC or self.bit[2].CCC): #CVVCC
        #{2.C.4)b)3]}
        
        if ps == 1 or not valid_init_cc(self.bit[2]):
          #{2.C.4)b)3]a]}
          return self.tokenize(end_of_brivla+1, SELBRI)
        else:
          #{2.C.4)b)3]b]}
          return self.tokenize(2, CMAVO)
      elif self.bit[0].C and self.bit[1].VhV and self.bit[2].CC: #CVhVCC
        #{2.C.4)b)4]}
        if ps != 1 and valid_init_cc(self.bit[2]):
          return self.tokenize(2, CMAVO)
        else:
          return self.tokenize(end_of_brivla+1, SELBRI )
      elif self.bit[0].C and self.bit[1].V and self.bit[2].counts_CC: #CVCC..
        #{2.C.4)b)5]]}
        if self.bit[3].V and end_of_brivla == 3: #CVCCV
          #{2.C.4)b)5]a]} - gismu
          return self.tokenize(4, SELBRI)
        
        if not valid_init_cc(self.bit[2]):
          #{2.C.4)b)5]b]}
          OKAY = True
          for bit in self.bit.items(end_of_brivla)[2:end_of_brivla]:
            if bit.CC and not valid_init_cc(bit):
              OKAY = False
          if OKAY:
            return self.tokenize(end_of_brivla+1, SELBRI)
        
        
        #{2.C.4)b)5]c]}
        first_v_is_ps = True
        for bit in self.bit.items(ps-1):
          if bit.has_V:
            first_v_is_ps = False
        if first_v_is_ps:
          return self.tokenize(end_of_brivla+1, SELBRI)
        
        
        #{2.C.4)b)5]d]}
        
        has_y = False
        i = 0
        for l in letters:
          i += 1
          if l.y:
            has_y = True
            break
        
        #has_y and !has_y are fairly similiar.
        # TODO : Consider merging these two cases?
        
        if has_y:
          #{2.C.4)b)5]d]}
          has_y = i-1
          letters = letters[:has_y] #Adjust letters to look at only stuff before the y
          i = 0
          
          #self.config.debug(letters)
          
          #{2.C.4)b)5]d]1>} - match (CVC){2,}y..
          CVC_MATCH = False
          while 1:
            #self.config.debug(i)
            if i+2 >= len(letters): #End of word... End of selbri..
              if i >= 3*2: #Then it's probably okay! But one more thing...
                CVC_MATCH = True
                return self.tokenize(end_of_brivla+1, SELBRI)
              break
            if letters[i+0].C and letters[i+1].V and letters[i+2].C:
              i += 3 #Match a CVC
            else:
              break #Okay, it's not a (CVC)*
            if i >= len(letters):
              break
          
          # And then make sure the CC's are all valid init pairs
          if CVC_MATCH:
            self.debug("CVC_MATCH")
            for bit in self.bits:
              self.debug(bit)
              if not valid_init_cc(bit.CC):
                self.debug("Has invalid init CC", bit.position)
                break
              elif bit.wordsep or bit.y:
                return self.tokenize(end_of_brivla+1, SELBRI)
          
          #{2.C.4)b)5]d]2>}
          frontmiddles = ["CVC", "CVV", "CV'V", "CCV"]
          ends = ["CVC", "CCVC", "CVCC"]
          
          i = 0
          while 1:
            if test(letters, i, ends, matchall):
              #Can match ZERO frontmiddles
              #So, it is a selbri!
              return self.tokenize(end_of_brivla+1, SELBRI)
            
            fms = test(letters, i, frontmiddles, match)
            if not fms:
              #{2.C.4)b)5]d]3>} - Doesn't match a front-middle
              return [self.tokenize(2, CMAVO), self.tokenize(has_y-2, SELBRI)] #XXX lujvo or fu'ivla
            i += fms
          
          
        else: #!has_y
          #{2.C.4)b)5]e]}
          i = 0
          
          while 1:
            #{2.C.4)b)5]e]1>} - If (CVC)}{2,}CV , break at first CV and make the rest a selbri
            
            #In other words
            #Starts with C. Ends with C.
            #Odd bits are V
            #Second-to-last is C, last is V
            #Even bits are CC, and those CC are valid
            # TODO (This parts' brother uses letters instead of bits, which seems nicer.)
            
            if i == 0: #Starts with C
              if not self.bit[0].C: #When would it ever start with a c?
                break
                
            elif i == end_of_brivla - 1: #Ends with CV
              if self.bit[end_of_brivla-1].CC and self.bit[end_of_brivla].V:
                #Actually, ends with CCV. Check that CC!
                if not(valid_init_cc(self.bit[end_of_brivla-1])):
                  break
                #First two are cmavo, rest is selbri
                return [self.tokenize(2, CMAVO), self.tokenize(end_of_brivla-1, SELBRI)]
              break
            elif i % 2 == 0: #Even bit, a CC
              if not self.bit[i].CC or not valid_init_cc(self.bit[i]):
                break
              #if not (self.bit[i].CC and valid_init_cc(self.bit[i])):
                #break
            else: #An odd bit. A single vowel.
              if not (self.bit[i].V):
                break
            i += 1
          
          
          #Try: nuncasnu
          
          #If any CC's are not valid_init_cc, then SELBRI
          old = None
          for bit in self.bit.items(end_of_brivla):
            if bit.counts_CC:
              #self.config.debug(bit, valid_init_cc(bit))
              if old:
                b = old.chars[-1].value
                c = bit.chars[0].value
                if not valid_init_cc([b, c]):
                  return self.tokenize(end_of_brivla+1, SELBRI)
              if not valid_init_cc(bit):
                return self.tokenize(end_of_brivla+1, SELBRI)
              else:
                old = bit #There might be a case of [CC][CC], in which case we'd need to check the C][C
            else:
              old = None
              
          
          
          #{2.C.4)b)5]e]2>}
          i = 0
          frontmiddles = ['CVC', 'CVV', 'CVhV', 'CCV'] 
          # NOTICE! I've added a CCV front-middle form, which isn't mentioned in brkwords.txt and so
          # is probably wrong. Despite the fact that it actually lets it parse everything.
          ends = ['CVhV', 'CVV', 'CCV', 'CCVCV', 'CVCCV']
          #miklAma
          #bakrecpa'o
          while 1:
            """
            Here is a regex-like form for what we're looking for:
              (Front_Middle)*(End)
            
            If the entire chunk matches that form, then it is a selbri. If not,
            then the first two bits make a cmavo, and the rest is a selbri.
            """
            end_test = test(letters, i, ends, matchall)
            if end_test: #XXX I guess... matchall -> mi klama & mi tsmuvla, match -> miklama mitsmuvla
              #Can match ZERO frontmiddles
              #So, it is a selbri!
              self.config.debug("{0}\n{1}".format(letters[i:], ends))
              
              if test(letters, i+end_test, ends, match):
                #There is more than one end, so it must be cmavo(CV) selbri()
                break
              else:
                return self.tokenize(end_of_brivla+1, SELBRI)
            
            
            
            frontmiddle_test = test(letters, i, frontmiddles, match)
            if not frontmiddle_test:
              #Doesn't match a front-middle
              break
              #return [self.tokenize(2, CMAVO), self.tokenize(has_y-2, SELBRI)]
            
            i += frontmiddle_test
            
            if i >= len(letters):
              self.config.error("How did I get here?", letters[0].position)
          
          
          #{2.C.4)b)5]e]3>}
          return self.tokenize(2, CMAVO), self.tokenize(end_of_brivla-1, SELBRI)
        #endif has_y
      else: #Some other begining we don't do nothing with!
        #{2.C.4)b)6]}
        self.config.warn("Don't know how to deal with this supposed selbri, it has a strange begining", self.bit[0].position)
        return self.tokenize(end_of_brivla+1, GARBAGE)
    
    
  
  def get_token(self):
    """
    This is the function that figures out what to do. It has many different possible return values:
      A Token instance: this is the Token it found
      A list of Token instances: multiple tokens needed to be handled at once, or the word breaking algorithm suggested to return multiple items
      An Ellipsis (notated as ...): this indicates that something happened behind the scenes, but it isn't ready to return a Token yet
      None: A token could not be created. It has probably reached the EOF.
    """
    if isinstance(self.bit[0], Token):
      #Something has already been tokenized, either upstream (perhaps the text is pre-parsed?),
      # or something that happened in this parser
      self.config.debug("Returning pre-parsed token {0}".format(self.bit[0]), self.bit[0].position)
      return self.bit.pop(0)
    
    if self.bit[0].garbage:
      self.config.strict("Found garbage")
      return self.tokenize(1, GARBAGE)
    
    if self.bit[0].whitespace:
      #{2.C.1)b)}
      r = self.tokenize(1, WHITESPACE)
      return r
    
    if self.bit[0].comma:
      #{None}
      self.config.warn("This comma is probably nonsensical", self.bit[0].position)
      return self.tokenize(1, GARBAGE)
    
    word_end = self.word()
    
    
    #{2.A}
    
    #if self.config.dotside and self.bit[0].period:
    #if self.bit[0].period:
      #word_end += self.word(word_end+1)
    if self.bit[0].period:
      return self.tokenize(1, PERIOD)
    if self.bit[word_end-1].has_C or (self.bit[word_end-1].period and (word_end >= 2 and self.bit[word_end-2].has_C)): #It's a cmene! OMG!
      #{2.A.1)}
      
      #The cmene must have a pause in front unless (not DOTSIDE and) there is a marker
      if not 'broken' and self.bit[0].period: #XXX if enabled, .i.a'odoklAmatidoidjan
        return self.tokenize(1, PERIOD), self.tokenize(word_end-1, CMENE)
      else:
        if self.config.dotside:
          self.config.strict("Dotside requires a period in front of cmene", self.bit[0].position)
        
        #{2.A.1)a)}
        #Requires a cmene marker: la, lai, la'i, doi
        i = word_end - 2 #We're looking for two bits, so we have to have space for two bits when we start
        found_vocative = False
        while i >= 0:
          if self.bit[i].value == 'l' and self.bit[i+1].value in ('a', 'ai', "a'i"):
            found_vocative = True
            #return self.tokenize(2, CMAVO), self.tokenize(word_end-2, CMENE)
          elif self.bit[i].value == 'd' and self.bit[i+1].value == 'oi':
            found_vocative = True
            #return self.tokenize(2, CMAVO), self.tokenize(word_end-2, CMENE)
          
          if found_vocative:
            #{2.A.1)b)}
            if i == 0: #ladjan
              return self.tokenize(2, CMAVO), self.tokenize(word_end-2, CMENE)
            if i > 0 and self.bit[i-1].has_V: #miviskaladjan
              #{2.A.1)b)}
              #Push this content up so that it may be handled later
              # XXX camxes says that miviskaladjan is a single cmene
              # Brkwords disagrees (morph_test:muSTElaVIson)
              marker = self.tokenize(2, CMAVO, start=i)
              name = self.tokenize(word_end-i-2, CMENE, start=i)
              
              #name = self.tokenize(word_end-i-1, CMENE, start=i+1)
              #marker = self.tokenize(2, CMAVO, start=i)
              self.bit.insert(i, marker)
              self.bit.insert(i+1, name)
              return ...
            #{2.A.1)c)}
          i -= 1
        
        #Didn't find a marker! Okay, so, let's just say the whole thing is a name?
        return self.tokenize(word_end, CMENE)
    
    
    
    #{2.A.3)}
    if self.bit[word_end-1].value == 'y':
      
      if self.bit[word_end].wordsep and not isinstance(self.bit[word_end], Token):
        if not self.bit[word_end].period:
          #Required to end with a pause
          self.config.strict("y at the end of a word is required to end with a pause", self.bit[word_end].position)
        else:
          self.bit.insert(word_end, self.tokenize(1, PERIOD, start=word_end+0))
      #y.
      
      
      i = word_end - 1
      didstuff = False
      while 1:
        i -= 1
        if i >= 0:
          #{2.A.3)a)} - lerfu, like by
          if self.bit[i].C:
            self.bit.insert(i, self.tokenize(2, CMAVO, start=i))
            i -= 2
            didstuff = True
            continue
          elif i > 0:
            #{2.A.3)b)} - another lerfu, y'y or the V'y
            #The CLL specifies the lerfu for "y" as {.y'y.}
            if self.bit[i].h and self.bit[i-1].value == 'y' or self.bit[i-1].V: #y'y
              if i <= 1: # or b:
                self.config.strict("[yV]'y must start with a pause", self.bit[word_end].position)
              self.bit.insert(i-1, self.tokenize(3, CMAVO, start=i-1))
              i -= 3
              didstuff = True
              continue
            elif self.bit[i].V and self.bit[i+1].y:
              #{2.A.3)c)}, {2.A.3)d)} - Vy
              if self.bit[i].value in ('i', 'u'):
                self.config.strict("iy and uy are reserved words", self.bit[i].position)
              self.bit.insert(i, self.tokenize(2, CMAVO, start=i))
              didstuff = True
              continue
        break
      if didstuff:
        return ...
      else:
        self.config.warn("Nothing happened when dealing with lerfu (%r)"%(self.bit.buffer), self.bit[0].position)
    
    #Take care of {2.A.3)b)} again, like ".y'ybu"
    if self.bit[1].y or self.bit[0].y:
      toks = []
      if self.bit[0].period:
        toks.append(self.tokenize(1, PERIOD))
        badform = False
      else:
        badform = True
      if self.bit[0].V or self.bit[0].y and self.bit[1].h and self.bit[2].y:
        toks.append(self.tokenize(3, CMAVO))
        if badform:
          self.config.strict("[yV]'y should start with a pause", self.bit[0].position)
      if toks:
        return toks
    
    #{2.A.2)}
    if self.bit[0].period and self.bit[1].y and self.bit[2].period:
      return self.tokenize(1, PERIOD), self.tokenize(1, HESITATION), self.tokenize(1, PERIOD)
    else:
      r = []
      while self.bit[0].y:
        r.append(self.tokenize(1, HESITATION))
      if r:
        return r
    
    
    
    if self.bit[0].period:
      #{1.}
      #TODO: Dotside/non-dotside
      p = self.tokenize(1, PERIOD)
      word_end = self.word()
      #self.config.debug("End of word:", self.bit[word_end], file=sys.stderr)
      
      return p
    
    
    cc, cc_location = self.locate_cc()
    #self.config.debug("cc:", cc, file=sys.stderr)
    #self.config.debug("ccl:", cc_location, file=sys.stderr)
    
    
    
    
    if cc == -1:
      #{2.B} and {2.B.1)} - no CC in first 5 letters
      #MUST be a cmavo
      #Break before each consonant
      #self.config.debug("forced cmavo")
      if self.bit[0].has_V:
        #i ue u'i
        return self.tokenize(1, CMAVO)
      elif self.bit[0].C:
        #doi do zo'o
        if self.bit[1].has_V:
          if self.bit[2].h:
            if self.bit[3].has_V: #zo'o, la'oi
              return self.tokenize(4, CMAVO)
            else:
              self.config.error("huh")
          else:
            return self.tokenize(2, CMAVO)
        #else:
          #raise Exception("What?")
    else:
      #Okay. There is a selbri somewhere in this mess...
      
      #miklAmalosofybakni
      
      if cc_location <= 5:
        r = self.break_a_selbri()
        assert r
        return r
      else:
        if self.bit[0].has_V: #alekArce
          return self.tokenize(1, CMAVO)
        elif self.bit[0].C: #lekArce
          #Break before the second C.
          i = 1
          while 1:
            i += 1
            if self.bit[i].has_C or self.bit[i].period:
              break
            elif i > 5:
              raise "what? NO...."
          return self.tokenize(i, CMAVO)

    self.config.debug("Buffer:"+str(self.bit.buffer))
    self.config.error("Nothing happened!", self.bit[0].position)
      
    if not self.bit.EOF:
      return self.tokenize(1, GARBAGE) #What is this nonsense?
    #else we have reached the EOF, and so will return None.

def Stream(config, stdin):
  bitbuf = orthography.Stream(config, stdin)
  valsibuf = ValsiParser(bitbuf, config)
  return valsibuf

def main():
  config = Configuration(sys.argv[1:])

  p = Stream(config, sys.stdin)
  
  if config.output_no_space:
    raise SystemExit("Space removal not implemented")
    for token in p:
      """
      If you can find two or more vowels in the token:
        Find the second to last one
        Make sure it is accented
        
      """
      pass
  else:
    for token in p:
      if not isinstance(token, BORING): # XXX Maybe "BORING" instead
        if config._debug:
          config.debug('yielding '+str(token))
        else:
          print(token, end=' ')
        sys.stdout.flush()

  print()


if __name__ == '__main__':
  main()