#!/usr/bin/python
# -*- coding: utf-8 -*-


DEBUG = True
def debug(*args):
  if DEBUG:
    print(*args)

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
    #Rule('a')*Rule('b')*Rule('c')
    #"Concat(Concat(a, b), c)" --> "Concat(a, Concat(b, c))"
    return Concat(self, other)

  def __pow__(self, other): #...
    #if other != "REPEAT":
    # raise Exception("Please multiply by string 'REPEAT'")
    return Repeat(self)

  def __add__(self, other): #&
    return AndOr(self, other)

  def __lshift__(self, other): #|
    return XOr(self, other)

  def match(self, tracker):
    ret = self.test(tracker)
    #
    tracker.config.debug("{0} --> {1}".format(self, ret))
    return ret


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
    #self.hit_count = 0
  def test(self, tracker):
    #self.hit_count += 1
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
  def test(self, tracker):
    tracker.config.debug("**** Entering Rule "+str(self))
    
    target = BNF[self]
    child_tracker = tracker.append_rule(self)
    result = target.match(child_tracker)
    #if repr(self) == 'selbri_3':
    if result == Match:
      tracker.config.debug("**** Exiting Rule "+str(self)+": ACCEPT with "+str(result)+' from '+str(target))
      tracker.accept_rule()
      return result
    else:
      tracker.config.debug("**** Exiting Rule "+str(self)+": FAILURE")
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

  def test(self, tracker):
    raise Exception(NotImplemented)


class AndOr(Condition):
  def test(self, tracker):
    A = self.terms[0].match(tracker)
    B = self.terms[1].match(tracker)
    if A == Match or B == Match:
      return Match
    elif A == NoFill or B == NoFill:
      return NoFill
    else:
      return NoMatch

class XOr(Condition): #Bad name, should be "Alternation" XXX
  #def __repr__(self):
    #return " {0}\n  |{1}".format(*self.terms)
  def test(self, tracker):
    tracker.checkin()
    a = self.terms[0].match(tracker)
    if a == Match:
      tracker.commit()
      return Match
    tracker.checkout()
    tracker.checkin()
    b = self.terms[1].match(tracker)
    
    if b:
      tracker.commit()
      return Match
    tracker.checkout()
    return NoMatch

class Concat(Condition):
  def test(self, tracker):
    """
    Possibilities:
        a; b->   Match   NoFill  NoMatch
        Match    Match   NoFill  NoMatch
        NoFill   NoFill  NoFill  NoMatch
        NoMatch  NoMatch NoMatch NoMatch
    If a is NoMatch, we know for sure there is NoMatch. Otherwise, we MUST test b.
    """
    a = self.terms[0].match(tracker)
    tracker.checkin()
    
    if a == NoMatch: #3,1; 3,2; 3,3 -> NoMatch
      tracker.config.debug("a"+repr(a))
      tracker.checkout() #A
      return NoMatch
    b = self.terms[1].match(tracker)
    tracker.config.debug("a"+repr(a))
    tracker.config.debug("b"+repr(b))
    if b == NoMatch: #1,3; 2,3 -> NoMatch
      tracker.checkout()
      return NoMatch
    
    tracker.commit()
    if a == b == Match: #1,1 -> Match
      return Match
    else: #1,2; 2,2; 2,1 -> NoFill
      return NoFill
    
  

class Repeat(Condition):
  def test(self, tracker):
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
  def test(self, tracker):
    term = self.terms[0]
    if term.match(tracker):
      return Match
    else:
      return NoFill
  #def __repr__(self):
    #r = "/%s/" % self.terms
    #return r

class Optional(Condition):
  def test(self, tracker):
    term = self.terms[0]
    ocv = tracker.current_valsi
    tracker.checkin()
    r = term.match(tracker)
    if r:
      tracker.commit()
      return r
    else:
      tracker.checkout()
      
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
