#!/usr/bin/python3.0
# -*- coding: utf-8 -*-

__version__ = "0" #I expect it will only get worst
__author__ = "djeims.roistn <purpleposeidon@gmail.com>"

"""
Needs a name.
  jbogerna  -  Lojbanic grammar
  brafi'e   -  Large fish (as opposed to cmafi'e)
  zirfi'e   -  Purple fish
  zirsam    -  Purple computer

I like {zirsam}

"""

import io
import sys
import inspect

import orthography
from orthography import valid_init_cc
from config import Configuration

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

def error(msg, pos, e=Exception):
  raise e("{0}: {1}".format(pos, msg))

def warn(msg, pos, e=Warning):
  print("{2} at {0}: {1}".format(pos, msg, e.__name__) , file=sys.stderr)





class Token:
  wordsep = True #So that if a Token is inserted into a Bit buffer, nothing will try to eat it
  h = False
  y = False
  
  counts_CC = False
  
  def __repr__(self):
    r = type(self).__name__+'('
    for i in self.bits:
      r += repr(i)
    return r+repr(self.bits[0].position)+')'
  
  def __str__(self):
    r = ''
    for b in self.bits:
      r += str(b)
    return "{0}({1})".format(type(self).__name__, r)
  
  def __init__(self, bits):
    self.bits = bits
    if not len(bits):
      error("Trying to tokenize nothing!")
    self.position = self.bits[0].position


class valsi(Token): pass

class cmene(valsi): pass
class cmavo(valsi): pass
class selbri(valsi): pass
class gismu(selbri): pass
class lujvo(selbri): pass
class fuhivla(selbri): pass

class boring(Token): pass #Ignore
class whitespace(boring): pass
class hesitation(boring): pass


class extra(Token): pass
class garbage(extra): pass
class period(extra, boring): pass


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
  
  #print("Using", match_function.__name__)
  for form in forms:
    
    if match_function(lets, pos, form):
      rs += [len(form)]
      #print(match_function.__name__, form, "to", lets[pos:])
      return len(form)
  if rs:
    return max(rs)
  #print("No", match_function.__name__, "for", forms, "in", lets[pos:])
    
  


class ValsiParser:
  def __init__(self, bit_iter, config):
    #This would be a good place to put arguments
    self.bit = bit_iter
    self.config = config
  
  def __iter__(self):
    while 1:
      try:
        v = self.get_token()
      except EOFError:
        if self.config.debug:
          print("EOF hit in ValsiParser", file=sys.stderr)
        return
      if v == ...:
        continue
      elif v == None or v == []:
        break
      elif type(v) == list:
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
      if self.config.debug:
        print("EOF touched in word()", file=sys.stderr)
      return i
    return i
  
  def locate_cc(self, start=0):
    #Return (Bit index of a CC or CyC, Non-h letters
    #Bit Index is indexed from 0, Non-h letters starts at 1.
    letter_count = 0
    while 1:
      try:
        cur = self.bit[start]
      except EOFError:
        return -1
      if cur.wordsep: #Errors? This used to be below the for
        return -1, letter_count+1
      
      if cur.counts_CC:
        return start, letter_count+1
      for c in cur.chars:
        if not c.h:
          letter_count += 1
      
      start += 1
  
  def find_accent(self, start=0):
    #Find the first accented letter. Return False if we find a wordsep instead.
    while 1:
      b = self.bit[start]
      if b.wordsep:
        return False
      if b.accented:
        return start
      start += 1
  
  def locate_ps(self, start):
    #{2.C.2)}
    #Returns the index of the penultimate stress
    if start-1 >= 0 and self.bit[start-1].accented:
      #{2.C.2)a)} and {2.C.2)b)}. 
      #a) is part because the selbri (or cmavo+selbri) always starts at 0 because everything in front
      #   has been broken off alerady
      #b) is satisfied because dipthongs are handled together
      return start - 1
    locus_ps = start
    
    
    
    #First check for explicit accents
    while 1:
      try:
        b = self.bit[locus_ps]
      except EOFError:
        break #Okay, so we hit the end of the text stream instead of finding an accent
      if b.wordsep:
        break
      if b.accented:
        return locus_ps
      
      locus_ps += 1
    
    #{2.C.2)c)}
    # XXX This doesn't match brkwords specifications
    
    
    word_end = self.word()
    
    first_v = word_end - 1
    while 1:
      if self.bit[first_v].has_V:
        break
      first_v -= 1
    
    second_v = first_v
    while 1:
      second_v -= 1
      if self.bit[second_v].has_V:
        return second_v
      elif second_v <= -1:
        raise Exception("Couldn't find a ps!\n{0}".format(self.bit.buffer))
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
        if self.config.debug:
          print(v, repr(b), self.bit.buffer)
          
        raise Exception("Tokenizing more than one word")
      v.append(b)
      count -= 1
    if self.config.token_error or self.config.print_tokens:
      print("TOKEN", t_type.__name__, v, file=sys.stderr)
    if self.config.token_error:
      raise Exception("Token Call Backtrace")
    if t_type == garbage and self.config.strict:
      error("Garbage token:", v)
    return t_type(v)
  
  
  
  def break_a_selbri(self):
    """This function is called when a CC is in the text. It deals with the rather massive issue of seperating selbri and cmavo. It returns either a single token, or a list of tokens. Should all fail, it will make the word a garbage token"""
    #{2.C.}
    
    accent = self.find_accent()
    ps = self.locate_ps(0)
    cc, cc_location = self.locate_cc()
    word_end = self.word()
    if self.config.debug:
      print("BUFFER:",self.bit.buffer, file=sys.stderr)
      print("cc_location:", cc_location, file=sys.stderr)
      print("PS:", ps, file=sys.stderr)
      print("cc:", cc, file=sys.stderr)
      print("we:", word_end, file=sys.stderr)
    
    
    letters = []
    for bit in self.bit.items(word_end):
      if bit.wordsep:
        break
      for char in bit.chars:
        letters.append(char)
    
    #Locate the end of the brivla
    
    end_of_brivla = ps
    alter_PS = False
    found_v = False
    while 1:
      end_of_brivla += 1
      try:
        bit = self.bit[end_of_brivla]
      except EOFError:
        print("EOF hit in break_a_selbri()", file=sys.stderr)
        end_of_brivla -= 1
        break #There's the end. Stops the while loop
      if bit.has_V:
        
        if bit.VhV:
          if end_of_brivla == self.word()-1:
            break
            
          else:
            ps = self.locate_ps(end_of_brivla)
            end_of_brivla = ps
        else:
          break
      if bit.wordsep:
        break #End of the word

    
    if self.config.debug:
      print("eb:", end_of_brivla, file=sys.stderr)
    
    
    #4.a - break off begining cmavo
    
    init_cmavo_tokens = []
    while self.locate_cc()[1] >= 5:
      #TODO: Don't assume
      if self.bit[0].has_V:
        init_cmavo_tokens.append(self.tokenize(1, cmavo))
      elif self.bit[0].has_C:
        init_cmavo_tokens.append(self.tokenize(2, cmavo))
      else:
        break
    if init_cmavo_tokens:
      return init_cmavo_tokens
    #print(has_starting_cc, file=sys.stderr)
    
    
    #4)3]
    if letters[0].V:
      find_first_consonant = 0
      for bit in self.bit:
        if bit.has_C:
          break
        if bit.whitespace:
          break
        find_first_consonant += 1
      
      #print("First C", self.bit[find_first_consonant]) #self.brit
      #print("valid cc?", valid_init_cc(self.bit[find_first_consonant]))
      #print("First con:", find_first_consonant)
      if self.bit[find_first_consonant].counts_CC: # and not valid_init_cc(self.bit[find_first_consonant]):
        #return self.tokenize(end_of_brivla+2, selbri) #XXX. This should be +1, not +2, so end_of_brivla is wrong somehow. TODO
        return self.tokenize(word_end, selbri) #XXX. This should be +1, not +2, so end_of_brivla is wrong somehow. TODO
      else:
        return self.tokenize(find_first_consonant, cmavo)
      
    else: #Okay, it starts with a consonant. And should have a CC by this point
      #print(self.bit.buffer)
      if self.bit[0].counts_CC or  (self.bit[0].C and self.bit[1].V and self.bit[2].CyC) : #CC... CVCyC...
        return self.tokenize(end_of_brivla+1, selbri)
      #elif self.bit[0].C and self.bit[1].V and self.bit[2].CCC:
        #return self.tokenize(end_of_brivla+1, selbri)
      elif self.bit[0].CyC:
        return self.tokenize(1, garbage)
      elif self.bit[0].C and self.bit[1].counts_VV and (self.bit[2].CC or self.bit[2].CCC): #CVVCC
        if ps == 1 or not(valid_init_cc(self.bit[2])):
          return self.tokenize(end_of_brivla+1, selbri)
        else:
          return self.tokenize(2, cmavo)
        
        #if not(self.bit[1].accented) and valid_init_cc(self.bit[2]):
          #return self.tokenize(2, cmavo)
        #else:
          #return self.tokenize(end_of_brivla+1, selbri)
      elif self.bit[0].C and self.bit[1].VhV and self.bit[2].CC:
        #print("We want to know about", self.bit[1])
        #print("The accent is at", ps)
        #print(self.bit.items(4))
        #print("The end is at:", end_of_brivla)
        
        if ps != 1 and valid_init_cc(self.bit[2]):
          return self.tokenize(2, cmavo)
        else:
          return self.tokenize(end_of_brivla+1, selbri)
      elif self.bit[0].C and self.bit[1].V and self.bit[2].counts_CC:
        if self.bit[3].V and end_of_brivla == 3: #CVCCV
          return self.tokenize(4, selbri)
        
        if not valid_init_cc(self.bit[2]):
          OKAY = True
          for bit in self.bit.items(end_of_brivla)[2:end_of_brivla]:
            if bit.CC and not valid_init_cc(bit):
              OKAY = False
          if OKAY:
            return self.tokenize(end_of_brivla+1, selbri) #TODO XXX uh, maybe this bit needs more review
        
        
        
        first_v_is_ps = True
        for bit in self.bit.items(ps-1):
          if bit.has_V:
            first_v_is_ps = False
        if first_v_is_ps:
          #print("SUPERB EOB+2 WARNING")
          #NOTE: Used to have end_of_brivla+1
          return self.tokenize(end_of_brivla+1, selbri) #Wait. Make this... make this... +2? WhY? :( TODO
        
        has_y = False
        i = 0
        for l in letters:
          i += 1
          if l.y:
            has_y = True
            break
        

        #has_y and !has_y are fairly similiar
        
        
        if has_y:
          #{2.C.4)b)5]d]}
          has_y = i-1
          letters = letters[:has_y]
          i = 0
          
          #print(letters)
          
          while 1:
            #match (CVC){2,} . (But it's really (CVC){2,}yMORRASTUFFA )
            #print(i)
            if i+2 >= len(letters): #End of word... End of selbri..
              if i >= 3*2: #Then it's okay!
                return self.tokenize(end_of_brivla+1, selbri)
              break
            if letters[i+0].C and letters[i+1].V and letters[i+2].C:
              i += 3 #Match a CVC
            else:
              break #Okay, it's not a (CVC)*
          
          
          frontmiddles = ["CVC", "CVV", "CV'V", "CCV"]
          ends = ["CVC", "CCVC", "CVCC"]
          
          i = 0
          while 1:
            if test(letters, i, ends, matchall):
              #Can match ZERO frontmiddles
              #So, it is a selbri!
              return self.tokenize(end_of_brivla+1, selbri)
            
            fms = test(letters, i, frontmiddles, match)
            if not fms:
              #Doesn't match a front-middle
              return [self.tokenize(2, cmavo), self.tokenize(has_y-2, selbri)] #XXX lujvo or fu'ivla
            i += fms
          
          
          
        else: #!has_y
          #{2.C.4)b)5]e]}
          i = 0
          
          while 1:
            #If there are at least two CVC's
            #And all the CC's are valid
            #ends with a CV
            #break first CV and CCV->\w
            
            #In other words
            #Starts with C. Ends with C.
            #Odd bits are V
            #Second-to-last is C, last is V
            #Even bits are CC, and those CC are valid
            if i == 0: #Starts with C
              if not self.bit[0].C: #When would it ever start with a c?
                break
                
            elif i == end_of_brivla - 1: #Ends with CV
              if self.bit[end_of_brivla-1].CC and self.bit[end_of_brivla].V:
                #Actually, ends with CCV. Check that CC!
                if not(valid_init_cc(self.bit[end_of_brivla-1])):
                  break
                #First two are cmavo, rest is selbri
                return [self.tokenize(2, cmavo), self.tokenize(end_of_brivla-1, selbri)]
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
            #if bit.counts_CC: print(bit, valid_init_cc(bit))
            if bit.counts_CC:
              if old:
                b = old.chars[-1].value
                c = bit.chars[0].value
                if not valid_init_cc([b, c]):
                  return self.tokenize(end_of_brivla+1, selbri)
              if not valid_init_cc(bit):
                return self.tokenize(end_of_brivla+1, selbri)
              else:
                old = bit #There might be a case of [CC][CC], in which case we'd need to check the C][C
            else:
              old = None
              
          
          
          i = 0
          frontmiddles = ['CVC', 'CVV', 'CVhV', 'CCV'] 
          # NOTICE! I've added a CCV front-middle form, which isn't mentioned in brkwords.txt and so is probably wrong. Despite the fact that it actually lets it parse everything.
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
            #{2.C.4)b)5]e]2>}
            end_test = test(letters, i, ends, matchall)
            if end_test: #XXX I guess... matchall -> mi klama & mi tsmuvla, match -> miklama mitsmuvla
              #Can match ZERO frontmiddles
              #So, it is a selbri!
              if self.config.debug:
                print(letters[i:])
                print(ends)
              if test(letters, i+end_test, ends, match):
                #There is more than one end, so it must be cmavo(CV) selbri()
                break
              else:
                return self.tokenize(end_of_brivla+1, selbri)
            
            
            
            frontmiddle_test = test(letters, i, frontmiddles, match)
            if not frontmiddle_test:
              #Doesn't match a front-middle
              break
              #return [self.tokenize(2, cmavo), self.tokenize(has_y-2, selbri)]
            
            i += frontmiddle_test
            
            if i >= len(letters):
              error("Wha' wha'? Where am I? I really need t' lay off tha' booze...")
          
          return self.tokenize(2, cmavo)
          #The below doesn't work with "miklAmado"
          #return [self.tokenize(2, cmavo), self.tokenize(word_end-2, selbri)]
          
          
      else: #Some other begining we don't do nothing with!
        return self.tokenize(end_of_brivla, garbage)
    
    return self.tokenize(end_of_brivla, garbage)
    
    
  def strict(self, message, position, e=None):
    if self.config.strict:
      error(message, position, e=Exception)
    else:
      warn(message, position, e=Warning)
  
  def get_token(self):
    """
    This is the function that figures out what to do. It has many different possible return values:
      A Token instance: this is the Token it found
      A list of Token instances: multiple tokens needed to be handled at once, or the word breaking algorithm suggested to return multiple items
      An Ellipsis (also called "..."): this indicates that something happened behind the scenes, but it isn't ready to return a Token yet
      None: A token could not be created. It has probably reached the EOF.
    """
    if isinstance(self.bit[0], Token):
      #Something has already been tokenized, either upstream (perhaps the text is pre-parsed?), or something that happened here.
      if self.config.debug:
        print("Returning pre-parsed token", self.bit[0], file=sys.stderr)
      return self.bit.pop(0)
    
    if self.bit[0].garbage:
      if self.config.strict:
        error("Strict. Found garbage")
      return self.tokenize(1, garbage)
    
    if self.bit[0].whitespace:
      r = self.tokenize(1, whitespace)
      return r
    
    
    
    word_end = self.word()
    
    
    #{2.A.1)}
    #if self.config.dotside and self.bit[0].period:
    if self.bit[0].period:
      word_end += self.word(word_end+1)
    
    #print(); print(word_end)
    if self.bit[word_end-1].has_C or (self.bit[word_end-1].period and (word_end >= 2 and self.bit[word_end-2].has_C)): #It's a cmene! OMG!
      #{2.A.1)a)}
      #The cmene must have a pause in front unless (not DOTSIDE and) there is a marker
      if self.bit[0].period:
        return [self.tokenize(1, period), self.tokenize(word_end-1, cmene)]
      else:
        if self.config.dotside:
          self.strict("Dotside requires a period in front of cmene (see --nodotside)", self.bit[0].position)
          
        #Requires a cmene marker: la, lai, la'i, doi
        i = word_end - 2 #We're looking for two bits, so we have to have space for two bits when we start
        found_token = False
        while i >= 0:
          if self.bit[i].value == 'l' and self.bit[i+1].value in ('a', 'ai', "a'i"):
            found_token = True
            #return [self.tokenize(2, cmavo), self.tokenize(word_end-2, cmene)]
          elif self.bit[i].value == 'd' and self.bit[i+1].value == 'oi':
            found_token = True
            #return [self.tokenize(2, cmavo), self.tokenize(word_end-2, cmene)]
          
          if found_token:
            #{2.A.1)b)}
            if i == 0: #ladjan
              return [self.tokenize(2, cmavo), self.tokenize(word_end-2, cmene)]
            if i > 0 and self.bit[i-1].has_V: #miviskaladjan
              #{2.A.1)b)}
              #Push this content up so that it may be handled later
              # (An old thought was to create a seperate parser to handle the text before what has been broken)
              
              marker = self.tokenize(2, cmavo, start=i)
              name = self.tokenize(word_end-i-2, cmene, start=i)
              
              #name = self.tokenize(word_end-i-1, cmene, start=i+1)
              #marker = self.tokenize(2, cmavo, start=i)
              self.bit.insert(i, marker)
              self.bit.insert(i+1, name)
              return ...
            #{2.A.1)c)}
          i -= 1
        
        #Didn't find a marker! Okay, so, let's just say the whole thing is a name?
        return self.tokenize(word_end, cmene)
    
    
    
    #{2.A.3)}
    #if self.config.debug:
      #print(self.bit.buffer, "@", word_end, file=sys.stderr)
    
    if self.bit[word_end-1].value == 'y':
      
      if self.bit[word_end].wordsep and not isinstance(self.bit[word_end], Token):
        if not self.bit[word_end].period:
          #Required to end with a pause
          self.strict("y at the end of a word is required to end with a pause", self.bit[word_end].position)
        else:
          self.bit.insert(word_end, self.tokenize(1, period, start=word_end+0))
      #y.
      
      
      i = word_end - 1
      didstuff = False
      while 1:
        i -= 1
        if i >= 0:
          #{2.A.3)a)} - lerfu, like by
          if self.bit[i].C:
            self.bit.insert(i, self.tokenize(2, cmavo, start=i))
            i -= 2
            didstuff = True
            continue
          elif i > 0:
            #{2.A.3)b)} - another lerfu, y'y or the V'y
            if self.bit[i].h and self.bit[i-1].value == 'y' or self.bit[i-1].V: #y'y
              if i <= 1: # or b:
                self.strict("[yV]'y must start with a pause", self.bit[word_end].position)
              self.bit.insert(i-1, self.tokenize(3, cmavo, start=i-1))
              i -= 3
              didstuff = True
              continue
            elif self.bit[i].V:
              #{2.A.3)c)}, {2.A.3)d)} - Vy
              if self.bit[i].value in ('i', 'u'):
                self.strict("iy and uy are reserved words", self.bit[i].position)
              self.bit.insert(i, self.tokenize(2, cmavo, start=i))
              didstuff = True
              continue
        break
      if didstuff:
        return ...
      else:
        warn("Nothing happened when dealing with lerfu", self.bit[0].position)
        print(self.bit.buffer)
    
    #Take care of {2.A.3)b)} again, like ".y'ybu"
    if self.bit[1].y or self.bit[0].y:
      toks = []
      if self.bit[0].period:
        toks.append(self.tokenize(1, period))
        badform = False
      else:
        badform = True
      if self.bit[0].V or self.bit[0].y and self.bit[1].h and self.bit[2].y:
        toks.append(self.tokenize(3, cmavo))
        if badform:
          self.strict("[yV]'y should start with a pause", self.bit[0].position)
      if toks:
        return toks
    
    #{2.A.2)}
    if self.bit[0].period and self.bit[1].y and self.bit[2].period:
      return [self.tokenize(1, period), self.tokenize(1, hesitation), self.tokenize(1, period)]
    else:
      r = []
      while self.bit[0].y:
        r.append(self.tokenize(1, hesitation))
      if r:
        return r
    
    
    
    if self.bit[0].period:
      #{1.}
      #TODO: Dotside/non-dotside
      p = self.tokenize(1, period)
      word_end = self.word()
      #print("End of word:", self.bit[word_end], file=sys.stderr)
      
      return p
    
    
    cc, cc_location = self.locate_cc()
    #print("cc:", cc, file=sys.stderr)
    #print("ccl:", cc_location, file=sys.stderr)
    
    
    
    
    if cc == -1:
      #MUST be a cmavo
      #Break before each consonant
      #print('forced cmavo', file=sys.stderr)
      if self.bit[0].has_V:
        #i ue u'i
        return self.tokenize(1, cmavo)
      elif self.bit[0].C:
        #doi do zo'o
        if self.bit[1].has_V:
          if self.bit[2].h:
            if self.bit[3].has_V: #zo'o, la'oi
              return self.tokenize(4, cmavo)
            else:
              error("huh")
          else:
            return self.tokenize(2, cmavo)
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
          return self.tokenize(1, cmavo)
        elif self.bit[0].C: #lekArce
          #Break before the second C.
          i = 1
          while 1:
            i += 1
            if self.bit[i].has_C or self.bit[i].period:
              break
            elif i > 5:
              raise "what? NO...."
          return self.tokenize(i, cmavo)
    
    error("Nothing happened!", self.bit[0].position)
      
    if not self.bit.EOF:
      return self.tokenize(1, garbage) #What is this nonsense?
    #else we have reached the EOF, and so will return None.


#def parse():
config = Configuration(sys.argv[1:])
charbuf = orthography.Buffer(orthography.stream_char(sys.stdin, config), config)
bitbuf = orthography.Buffer(orthography.stream_bit(charbuf), config)
p = ValsiParser(bitbuf, config)

for token in p:
  if not isinstance(token, boring):
    print(token, end=' ')

print()


#parse()