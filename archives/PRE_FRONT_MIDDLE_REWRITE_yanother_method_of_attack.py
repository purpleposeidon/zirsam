#!/usr/bin/python3.0
# -*- coding: utf-8 -*-


"""
maicpukai  - XXX means 'gravity', but it don't parse by this or jbofihe
samsincyfi'e
"""

import io
import sys
import inspect

"""
Desired cl options:
  Input Options
    STRICT - Pure lojban
    MIXED - Hunt down lojban text in otherwise english text?
    AUTOQUOTE - Automatic quote of obviously foreign texts?
    
  Parsing Options
    NOWARN - Don't warn about usage errors
    DOTSIDE - Require names to be dotsid'd
    NOSU - Speed up parsing by not needing to cache the entire text?
    NOSI - Kinda like NOSU. But it only caches 2 sentances.
    INTEPRET - Substitute out pro-sumti (Or maybe this is OUTPUT?)
    BADGARBAGE - error on garbage
    EXTENDED - Include (experimental) language extensions
    
  Output Options
    NORMALIZE - Output normalized lojban (Elided terminators, space-sep words, zo'e instead of SE/FA)
    REPAIR - Fix errors
    1337 - Output 31337 lojban
    SMOOSH - No spaces
    GRAVE - Use fancy accent marks in output
    TRANSLATE - attempt translation
    STRUCTURE - show strucutre
    
  
  Warning options:
    Cultural items
    Use of la
  
"""


#TODO: Single characters that expand to multiple characters
{'1':'pa', '2':'re', '3':'ci', '4':'vo', '5':'mu', '6':'xa', '7':'ze', '8':'bi', '9':'so', '0':'no'}
#Also: diaerisies. I think, also + - / *, =?

def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_back.f_lineno


def error(msg, pos=None, e=Exception):
  print( e("%s: %s" % (pos, msg)) , file=sys.stderr)

def warn(msg, pos=None, e=Warning):
  raise e("%s: %s" % (pos, msg))


class ParserOptions:
  """
  Default to NICE and NOISY
  """
  def __init__(self, args=sys.argv):
    self.strict = False
    self.quiet = False
    self.print_tokens = False
    self.dotside = True
    self.ascii_only = False
    self.token_error = False
    
    
    if '--strict' in sys.argv:
      self.strict = True
    if '--ascii' in sys.argv:
      self.ascii_only = True
    if '--quiet' in sys.argv:
      self.quiet = True
    if '--print-tokens' in sys.argv:
      self.print_tokens = True
    if '--token-error' in sys.argv:
      self.token_error = True



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
    return "Line: %s Col: %s" % (self.lin, self.col)
  def __repr__(self):
    return '+%s:%s' % (self.lin, self.col)
  def pushline(self):
    self.c += 1
    self.col = 0
    self.lin += 1
  def pushcol(self):
    self.c += 1
    self.col += 1


class Buffer:
  def __repr__(self):
    return "<Buffered %s>" % (self.iterable)
  def __init__(self, iterable):
    self.iterable = iterable
    self.buffer = []
    self.EOF = False
  
  def __feed_buffer(self):
    """Add a single item to the buffer"""
    if self.EOF:
      raise EOFError()
    try:
      self.buffer.append(self.iterable.__next__())
    except (EOFError, StopIteration) as e:
      #print(self, "got eof error:", e)
      self.EOF = True
    finally:
      if self.EOF:
        raise EOFError()
  
  def __fill_to(self, index):
    while index + 1 > len(self.buffer):
      self.__feed_buffer()
  
  def __iter__(self):
    i = 0
    while 1:
      yield self[i]
      i += 1
      
  def items(self, num):
    self.__fill_to(num)
    return self.buffer[:num]
  
  def __getitem__(self, index):
    self.__fill_to(index)
    return self.buffer[index]
  
  def pop(self):
    self.__fill_to(0)
    return self.buffer.pop(0)



__VALID_INIT_CC = "bl br cf ck cl cm cn cp cr ct dj dr dz fl fr gl gr jb jd jg jm jv kl kr ml mr pl pr sf sk sl sm sn sp sr st tc tr ts vl vr xl xr zb zd zg zm zv".split(' ')
def valid_init_cc(bit):
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


class Character:
  whitespace = ' \t\n\r'
  low_vowel = 'aeiou'
  
  #NOTE: Sane people don't use macrons
  A = "AáÁàÀ" #āĀ
  E = "EéÉèÈ" #ēĒ
  I = "IíÍìÌ" #īĪ
  O = "OóÓòÒ" #ōŌ
  U = "UúÚùÙ" #ūŪ
  accent_vowel = A+E+I+O+U
  con = 'bcdfgjklmnprstvxz'
  y = 'yY'
  h = "'h\"H"
  comma = ','
  period = "."
  
  
  def clean_val(v):
    #Escapes stuff if neccessary. "\n" -> "\\n"
    if '\\' in repr(v):
      return repr(v)[1:-1]
    else:
      return str(v)
  
  def __repr__(self):
    return str(self)
    #return "<%r %s>" % (self.value, self.position)
  
  def __str__(self):
    return Character.clean_val(self.value)
  
  def __init__(self, c, position=None):
    self.original = c
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
    
    if c == '':
      self.EOF = True
      self.value = ''
    elif c in Character.accent_vowel:
      if c in Character.A: self.value = 'A'
      elif c in Character.E: self.value = 'E'
      elif c in Character.I: self.value = 'I'
      elif c in Character.O: self.value = 'O'
      elif c in Character.U: self.value = 'U'
      else: wtf
      self.accented = True
      self.V = True
    elif c in Character.low_vowel:
      self.value = c
      self.V = True
    elif c.lower() in Character.con:
      self.value = c.lower()
      self.C = True
    elif c in Character.y:
      self.value = 'y'
      self.y = True
    elif c in Character.comma: 
      self.value = ','
      self.comma = True
    elif c in Character.period:
      self.value = '.'
      self.period = True
    elif c in Character.h:
      self.value = "'"
      self.h = True
    elif c in Character.whitespace:
      self.value = c
      self.whitespace = True
    else:
      self.garbage = True
      self.value = c
    self.value

def stream_char(fd):
  p = Position()
  while 1:
    c = fd.read(1)
    if c == '\n':
      p.pushline()
    elif c:
      p.pushcol()
    
    if c == '':
      yield Character('', Position(p))
      break
    else:
      yield Character(c, Position(p))

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
        if fd[1].C: #CCC
          self.CCC = True
          self.counts_CC = True
          self.chars = [first, fd.pop(), fd.pop()]
        else: #CC
          self.CC = True
          self.counts_CC = True
          self.chars = [first, fd.pop()]
      elif fd[0].y and fd[1].C: #CyC
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
      if char.V or char.C:
        self.cc_letter_counts += 1
    
    self.position = self.chars[0].position


class Token:
  def __repr__(self):
    r = type(self).__name__+'('
    for i in self.bits:
      r += repr(i)
    return r+repr(self.bits[0].position)+')'
  
  def __str__(self):
    r = ''
    for b in self.bits:
      r += str(b)
    return "%s(%s)" % (type(self).__name__, r)
  
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


class extra(Token): pass
class garbage(extra): pass
class period(extra): pass

class boring(Token): pass
class whitespace(boring): pass
class hesitation(boring): pass


class ValsiParser:
  def __init__(self, bit_iter):
    #This would be a good place to put arguments
    self.bit = bit_iter
  
  def __iter__(self):
    while 1:
      try:
        v = self.get_token()
      except EOFError:
        #print("EOF", file=sys.stderr)
        return
      if v == None or v == []:
        break
      elif type(v) == list:
        for extra_token in v:
          yield extra_token
      else:
        yield v
  
  #Utilities for ValsiParser.bit
  def word(self):
    #Returns the number of bits that are part of the word
    i = 0
    try:
      while not self.bit[i].wordsep:
        i += 1
    except EOFError:
      print("EOFWARN", file=sys.stderr)
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
      if cur.counts_CC:
        return start, letter_count+1
      for c in cur.chars:
        if not c.h:
          letter_count += 1
      if cur.wordsep:
        return -1, letter_count+1
      
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
  
  def letters(self, count):
    #Returns a list of the first count letters.
    r = []
    i = 0
    while i <= count:
      for letter in self.bit.buffer[i].chars:
        r.append(letter)
      i += 1
    return r
  
  def ALT_locate_ps(self, start="IGNORED"):
    #Another way to try it. 
    
    #Returns the index of the stress
    #It is either an ACCENTED letter
    #Or the second-to-last vowel
    i = self.word()
    FOUND_ACCENT = None
    ACCENT_OVERIDE = False
    vowel_count = 0 #Going backwards...
    while i >= 0:
      if self.bit[i].has_V:
        vowel_count += 1
      if vowel_count == 2 and ACCENT_OVERIDE == False:
        FOUND_ACCENT = i
      
      if self.bit[i].accented:
        FOUND_ACCENT = i
        ACCENT_OVERIDE = True
      i -= 1
    return FOUND_ACCENT+1
  
  def locate_ps(self, start):
    #Returns the index of the penultimate stress
    if start-1 >= 0 and self.bit[start-1].accented:
      #Includes a) and b)
      return start - 1
    locus_ps = start
    
    #Stop early if we find an accent
    while 1:
      try:
        b = self.bit[locus_ps]
      except EOFError:
        break #Okay, so we hit the end of the text stream instead of finding an accent
      if b.accented:
        return locus_ps
      if b.wordsep:
        break
      locus_ps += 1
      
    #Find the second-to-last vowel thingie
    ##Find first the end of the word
    word_end = self.word()
    
    first_v = word_end
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
        raise Exception("Couldn't find a ps!\n%s" % self.bit.buffer)
    return False
  
  def tokenize(self, count, t_type):
    #Pops count letters (1-indexed) from ValsiParser.bit, and creates a Token object (as given by t_type). The token is returned.
    #If -bt is given as an argument, then it will raise an error
    v = []
    assert count > 0
    while count:
      b = self.bit.pop()
      if len(v) and b.wordsep:
        raise Exception("Tokenizing more than one word")
      v.append(b)
      count -= 1
    if '-st' in sys.argv:
      print("TOKEN", t_type.__name__, v, file=sys.stderr)
    if '-bt' in sys.argv:
      if not '-st' in sys.argv:
        print("TOKEN", t_type.__name__, v, file=sys.stderr)
      raise Exception("Token Call Backtrace")
    return t_type(v)
  
  
  
  def break_a_selbri(self):
    """This function is called when a CC is in the text. It deals with the rather massive issue of seperating selbri and cmavo. It returns either a single token, or a list of tokens. Should all fail, it will make the word a garbage token"""
    
    accent = self.find_accent()
    ps = self.locate_ps(0)
    cc, cc_location = self.locate_cc()
    word_end = self.word()
    if '-bt' in sys.argv:
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
        print("EOFERROR", file=sys.stderr)
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
      
    '''for bit in self.bit.items(self.word()):
      
      
      print("ALIVE", bit, end_of_brivla, sys.stderr)
      if bit.has_V:
        found_v = True
        if bit.VhV:
          #Uh oh, weird stuff! {3)b)}
          ps = self.locate_ps(end_of_brivla)
        else:
          break
      if bit.wordsep:
        break
      end_of_brivla += 1'''
    
    #if not found_v:
      #self.error("Must have a vowel after a stress")
    
    if '-bt' in sys.argv:
      print("eb:", end_of_brivla, file=sys.stderr)
    
    #if self.bit[ps].VhV:
      #end_of_brivla -= 1
    
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
      for bit in self.bit.items(4):
        if bit.has_C:
          break
        find_first_consonant += 1
      
      #print("First C", self.bit[find_first_consonant]) #self.brit
      #print("valid cc?", valid_init_cc(self.bit[find_first_consonant]))
      if self.bit[find_first_consonant].CC and not valid_init_cc(self.bit[find_first_consonant]):
        return self.tokenize(end_of_brivla+2, selbri) #XXX. This should be +1, not +2, so end_of_brivla is wrong somehow. TODO
      else:
        return self.tokenize(find_first_consonant, cmavo)
      
    else: #Okay, it starts with a consonant. And should have a CC by this point
      if self.bit[0].CC or  (self.bit[0].C and self.bit[1].V and self.bit[2].CyC)  : #CVCyC...
        return self.tokenize(end_of_brivla+1, selbri)
      elif self.bit[0].CyC:
        return self.tokenize(1, garbage)
      elif self.bit[0].C and self.bit[1].counts_VV and self.bit[2].counts_CC: #CVVCC
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
          has_y = i
          letters = letters[:has_y]
          i = 0
          while 1:
            #match CVC
            if i >= len(letters): #End of word... End of selbri..
              if i >= 3*2:
                return self.tokenize(end_of_brivla, selbri)
            if letters[i+0].C and letters[i+1].V and letters[i+2].C:
              i += 3 #Match a CVC
            else:
              break #Okay, it's not a (CVC)*
          
          i = 0
          while 1:
            #match front-middles
            #CVC CVV CV'V CCV
            does_pass = False
            if letters[i].C:
              if letters[i+1].V:
                if letters[i+2].C or letters[i+2].V:
                  does_pass = 3
                elif letters[i+2].h and letters[i+3].V:
                  does_pass = 4
              elif letters[i+1].C:
                if letters[i+2].V:
                  does_pass = 3
            if does_pass:
              i += does_pass
            else:
              #Okay, maybe it's secretly the end
              #CVC CCVC CVCC
              YES = False
              if letters[i].C:
                if letters[i+1].V:
                  if letters[i+2].C:
                    YES = 2
                    if letters[i+3].C:
                      YES = 3
                      print(lineno(), file=sys.stderr)
                    else:
                      print(lineno(), file=sys.stderr)
                elif letters[i+1].C:
                  if letters[i+2].V:
                    if letters[i+3].C:
                      YES = 3
                      print(lineno(), file=sys.stderr)
              
              if not YES:
                return self.tokenize(self.word(), selbri) #{2.C.4)b)5]d]2>}. Seems valid.
              else:
                #Uh, that starting CV is a cmavo, and the rest is a selbri
                return [self.tokenize(2, cmavo), self.tokenize(has_y-2, selbri)]
          
        else: #!has_y
          i = 0
          #besmamta
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
          for bit in self.bit.items(end_of_brivla):
            if bit.counts_CC and not valid_init_cc(bit):
              return self.tokenize(end_of_brivla+1, selbri)
          
            
          #A thought: It'd be nice to be able to check from the end first.    
          
          lentest = lambda N: len(letters) - 1 >= N
          #xisli'icutci
          i = 0
          while 1:
            #match front/middles
            #CVC CVV CV'V
            does_pass = False
            #need either i+2 letters or (maybe) i+3 letters
            if lentest(i+2) and letters[i].C:
              #len(letters) - 1 >= i+2:
              if letters[i+1].V:
                if letters[i+2].C:
                  does_pass = 3
                elif letters[i+2].V:
                  does_pass = 3
                else:
                  if letters[i+2].h and lentest(i+3) and letters[i+3].V:
                    does_pass = 4
            
            if len(letters) <= i+does_pass:
              does_pass = False
            if does_pass:
              i += does_pass
            else:
              if type(does_pass) == int:
                raise Exception("Ohcrap")
              #Okay, maybe it's secretly the end
              #CVV CV'V CVCCV CCV CCVCV
              YES = 0
              del YES
              def YEZ():
                print(lineno(), file=sys.stderr)
              print("At location", i, file=sys.stderr)
              print(letters, file=sys.stderr)
              #xisli'icutci
              if lentest(i+2) and letters[i+0].C:
                #len(letters) - 1 >= i+2:
                if letters[i+1].V:
                  if letters[i+2].V:
                    YES = 2 #CVV
                    YEZ()
                  elif lentest(i+3): #len(letters) - 1 >= i+3:
                    if letters[i+2].h and letters[i+3].V:
                      YES = 3 #CVhV
                      YEZ()
                    elif lentest(i+5) and \
                    letters[i+3].C and letters[i+4].C and letters[i+5].V:
                      #len(letters) - 1 >= i+5:
                      YES = 5 #CVCCV
                      YEZ()
                    else:
                      YES = False;YEZ()
                  else:
                    YES = False;YEZ()
                elif letters[i+1].C and letters[i+2].V:
                  if lentest(i+4) and \
                  letters[i+3].C and letters[i+4].V:
                    YES = 4 #CCVCV
                    YEZ()
                  else:
                    YES = 2
                    YEZ()
                else:
                  YES = False;YEZ()
              else:
                print("Fails:", letters[i], lentest(i+2), i)
                YES = False;YEZ()
                
              if YES:
                return self.tokenize(end_of_brivla+1, selbri)
              else:
                #Uh, that starting CV is a cmavo, and the rest is a selbri
                return self.tokenize(2, cmavo)
                #return [self.tokenize(2, cmavo), self.tokenize(has_y-2, selbri)]
          
          error("I couldn't figure out how to match anything! Is this even possible!?!?")  
          
      else: #Some other begining we don't do nothing with!
        return self.tokenize(end_of_brivla, garbage)
    
    return self.tokenize(end_of_brivla, garbage)
    
    
    
  
  def get_token(self):
    """Returns either a single token or a list of tokens or None if there is nothing left."""
    if self.bit[0].garbage:
      return self.tokenize(1, garbage)
    if self.bit[0].whitespace:
      r = self.tokenize(1, whitespace)
      return r
    elif self.bit[0].period:
      #TODO: Dotside/non-dotside
      p = self.tokenize(1, period)
      word_end = self.word()
      #print("End of word:", self.bit[word_end], file=sys.stderr)
      
      return p
    else:
      word_end = self.word()
      if self.bit[word_end].has_C or (self.bit[word_end].period and self.bit[word_end-1].has_C): #It's a cmene! OMG!
      
        return self.tokenize(word_end, cmene)
    
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
        return self.break_a_selbri()
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
      
      
    if not self.bit.EOF:
      return self.tokenize(1, garbage) #What is this nonsense?
    #else we have reached the EOF, and so will return None.


#def parse():
charbuf = Buffer(stream_char(sys.stdin))
bitbuf = Buffer(stream_bit(charbuf))
p = ValsiParser(bitbuf)

for token in list(p):
  if not isinstance(token, boring):
    print(token, end=' ')

print()
"""
Standard:
  Repr should convey more information
  Str should be prettier

"""

#parse()