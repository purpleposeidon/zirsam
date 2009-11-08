#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
Match:
  {pa re ci} into <PA ...>
NoFill:
  {} into <PA ...>
NoMatch:
  {gletu} info <PA ...>
"""
#Logic values
class LogicValue:
  def __repr__(self): return self.n
  def __init__(self, n, b): self.n, self.b = n, b
  def __bool__(self): return self.b
  def __or__(self, other): return bool(self) | bool(other)
  def __ror__(self, other): return bool(self) | bool(other)
  def __and__(self, other): return bool(self) & bool(other)
  def __rand__(self, other): return bool(self) & bool(other)
  def __xor__(self, other): return bool(self) ^ bool(other)
  def __rxor__(self, other): return bool(self) ^ bool(other)
Match = LogicValue('Match', True)
NoFill = LogicValue('NoFill', True) #For empty repeats and elidable terminators
NoMatch = LogicValue('NoMatch', False)


BNF = None  #This will be set by bnf/__init__.py; it is used by the Rule.

class BnfObjectBase:
  #All bnf items will need these methods
  def __mul__(self, other): #sepearted by whitespace
    return Concat(self, other)

  def __pow__(self, other): #...
    if other != "REPEAT":
     raise Exception("Please multiply by string 'REPEAT'")
    return Repeat(self)

  def __add__(self, other): #&
    return AndOr(self, other)

  def __lshift__(self, other): #|
    return XOr(self, other)



class Term(BnfObjectBase):
  def __hash__(self):
    return hash(self.content)
  #def __eq__(self, other):
    #return hash(self) == hash(other)
  def __repr__(self):
    return self.type+'('+str(self.content)+')'
    
  def __init__(self, content):
    self.content = content
    self.type = type(self).__name__



class Terminal(BnfObjectBase):
  def __repr__(self):
    return str(self.selmaho)
  def __init__(self, selmaho):
    self.selmaho = selmaho
    self.hit_count = 0
  def match(self, tracker):
    self.hit_count += 1
    #if self.hit_count > 10:
      #raise Exception
    try:
      a = tracker.valsi[tracker.current_valsi] #.type
    except (EOFError, StopIteration) as e:
      return NoMatch
    
    if a.type == self.selmaho:
      tracker.accept_terminal()
      return Match
    elif type(self.selmaho) == type and isinstance(a, self.selmaho):
      tracker.accept_terminal()
      return Match
    else:
      return NoMatch

class Rule(BnfObjectBase):
  def match(self, tracker):
    #print("**** Entering Rule", self)
    
    target = BNF[self]
    child_tracker = tracker.append_rule(self)
    result = target.match(child_tracker)
    ##print(self, result, target)
    #if repr(self) == 'selbri_3':
      #print("~!!!! selbri_3 RESULT:", result)
    #print(self, result)
    if result == Match:
      #print("**** Exiting Rule", self, ": ACCEPT", "with", result, 'from', target)
      tracker.accept_rule()
      return result
    else:
      #print("**** Exiting Rule", self, ": FAILURE")
      child_tracker.fail()
      return NoMatch
    
      
    

  def __repr__(self):
    return self.name
  def __str__(self): return self.name
  def __hash__(self):
    return hash(self.name)
  def __eq__(self, other):
    return str(self) == str(other)
  def __init__(self, rule_name):
    self.name = rule_name
    #self.dirty = False


class Condition(BnfObjectBase):
  def __repr__(self):
    r = type(self).__name__+repr(tuple(self.terms))
    return r
  
  def __init__(self, *terms):
    self.terms = terms

  def match(self, tracker):
    raise Exception(NotImplemented)


class AndOr(Condition):
  def match(self, tracker):
    A = self.terms[0].match(tracker)
    B = self.terms[1].match(tracker)
    ##print(self, A, B)
    if A == Match or B == Match:
      return Match
    elif A == NoFill or B == NoFill:
      return NoFill
    else:
      return NoMatch

class XOr(Condition): #Bad name, should be "Alternation"
  #def __repr__(self):
    #return " {0}\n  |{1}".format(*self.terms)
  def match(self, tracker):
    a = self.terms[0].match(tracker)
    if a:
      ##print('   |', self, a)
      return Match
    
    b = self.terms[1].match(tracker)
    ##print('   |', self, b)
    if b:
      
      return Match
    return NoMatch

class Concat(Condition):
  def match(self, tracker):
    a = self.terms[0].match(tracker)
    tracker.checkin()
    if not a:
      ##print(self, '@', self.terms, a)
      tracker.checkout() #A
      return NoMatch
    b = self.terms[1].match(tracker)
    if b:
      ##print(self, '@', self.terms, 'Match')
      tracker.commit()
      return Match
    ##print(self, '@', self.terms, b)
    
    tracker.checkout()
    '''
    if 'A(e)' in str(tracker):
      import code
      ic = code.InteractiveConsole(locals())
      tracker.checkout()
      tracker.checkin()
      #ic.interact()
    '''
    return b
    
  

class Repeat(Condition):
  def match(self, tracker):
    """
    Return either NoRepat or Match.
    If it matches more than once, return Match
    
    """
    term = self.terms[0]
    t1 = term.match(tracker)
    if t1 == Match:
      #We are golden, no matter what
      i = 1
      while term.match(tracker) == Match:
        #Continue matching; only stop if something is obviously broken.
        i += 1
        if i == 2000:
          raise Exception("A repeat of more than {0} items is ridiculous. (in {1})".format(i, self)) #For debugging
      return Match
    else:
      #Didn't match even once, but it is still matches
      return NoFill
    return once

class Elidable(Condition):
  def match(self, tracker):
    #print("!Careful!", self)
    term = self.terms[0]
    if term.match(tracker):
      return Match
    else:
      return NoFill
  #def __repr__(self):
    #r = "/%s/" % self.terms
    #return r

class Optional(Condition):
  def match(self, tracker):
    term = self.terms[0]
    ocv = tracker.current_valsi
    tracker.checkin()
    r = term.match(tracker)
    #print("Original cv", ocv, 'present cv', tracker.current_valsi, 'parent cv', tracker.parent.current_valsi)
    if r:
      tracker.commit()
      return Match
    else:
      tracker.checkout()
      #print(tracker)
      #print("&&&& I am not getting rid of my crap!")
      #print("Got", r)
      #print("vvv There should be a console down here soon")
      
      #if 'A(e)' in str(tracker):
        #import code
        #ic = code.InteractiveConsole(locals())
        #ic.interact()
      return NoFill
  #def __repr__(self):
    #r = "[%s]" % self.terms
    #return r





"""
indicator = (Terminal(UI)<<Terminal(CAI))*Optional(Terminal(NAI))<<Terminal(Y)<<Terminal(DAhO)<<Terminal(FUhO)

indicator =
    (UI | CAI) [NAI]
    | Y
    | DAhO
    | FUhO

XOr(UI, CAI, Y, DAhO, FUhO) [NAI]
...wrong!
Should be
XOr(Xor(UI, CAI) [NAI], Y, DAhO, FUhO)
"""
