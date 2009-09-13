#!/usr/bin/python3.0
# -*- coding: utf-8 -*-

"""
Usage:
  ./bnfgen.py > bnf.py
"""

import io
import time, os, sys

sys.path.append('../')

change = os.path.split(sys.argv[0])[0]
if change:
  os.chdir(change) #Chdir to script location

from tokens import *

"""
Converts data/lojban.bnf to python structure. Run
  python bnfparser.py > bnf.py

When converting it over, I don't use the same operators that would be expected.
  Rule("foo")^REPEATED & Rule("bar")
is actually
  Term("foo")^ (REPEATED & Term("bar"))
Which don't do. So, instead, use....
  Term("foo")+REPEATED & Term("bar")
"""


#NOTE : Some of these are written NAME##, where the name is actually "NAME#", and
#       the trailing numbers are references to yac rule #

src = """
sumti-tail111 =
    [sumti-6 [relative-clauses]] sumti-tail-1
    | relative-clauses sumti-tail-1 ;
"""


TESTsrc = """
statement-314 =
sentence
 | [tag] TUhE # text-1 /TUhU#/ ;
"""

TESTsrc = """
test = a | b ... & c#;
"""

src = open('../data/lojban.bnf').read()

#from sys import stdout
stdout = io.StringIO()

def gen_rule(r):
  in_elidable = False
  while r:
    if r[0] in letters:
      n = ''
      while r and r[0] in letters:
        n += r[0]
        r = r[1:]
      if n.replace('h', 'H') == n.upper():
        #Is a terminal
        stdout.write("Terminal(%s)" % str(n))
      else:
        stdout.write("Rule(%s)" % repr(n))
    elif r[0] in '[':
      stdout.write("Optional(")
      r = r[1:]
    elif r[0] in '(':
      stdout.write("Paren(")
      r = r[1:]
    elif r[0] in '|':
      stdout.write(" |")
      r = r[1:]
    elif r[:3] in '...':
      r = r[3:]
      stdout.write(" +REPEATED")
    elif r[0] in '])':
      stdout.write(")")
      r = r[1:]
    elif r[0] in ' \n\t':
      stdout.write(", ")
      while r[0] in ' \n\t':
        r = r[1:]
    elif r[0] in '#':
      r = r[1:]
      stdout.write(', Optional(Rule("free")+REPEATED)')
    elif r[0] in '&':
      stdout.write(' & ')
      r = r[1:]
    elif r[0] in '/':
      r = r[1:]
      in_elidable = not in_elidable
      if in_elidable:
        stdout.write('Elidable(')
      else:
        stdout.write(")")
    else:
      raise Exception("Can't handle character %r" % r[0])

from string import ascii_letters as letters
letters = letters+'-'+'1234567890'

def variable(r):
  #If everything is lowercase, then it is a rule. If everything but h is capitalized, it is a terminator
  if r.lower() == r:
    return Rule(r)
  elif r.replace('h', 'H') == r.upper():
    return Terminal(r)
  else:
    raise Exception("The %r, is it a Rule or a Terminal?" % r)

class Rule:
  def __init__(self, value):
    self.value = value

class Token:
  def __init__(self, value):
    self.value = value

def parse(src):
  while '  ' in src:
    src = src.replace('  ', ' ')
  rule_list = src.split(';')
  stdout.write("rules = {\n")
  for srcrule in rule_list:
    srcrule = srcrule.replace('\n', ' ')
    srcrule = srcrule.strip()
    if not srcrule:
      continue
    rule_name, rule_body = (_.strip() for _ in srcrule.split('='))
    stdout.write('\t'+repr(rule_name)+': (')
    gen_rule(rule_body)
    stdout.write('), \n')
  stdout.write("}")

class MAGIC_ADD:
  """ <an expression> ^ MAGIC_ADD_INSTANCE(foo) gives foo(<an expression>) """
  def __init__(self, ob):
    self.tocall = ob
  def __radd__(self, other):
    return self.tocall(other)

def tree_type(name):
  class klass:
    pass
  def __init__(self, *items):
    self.items = items
  def __or__(self, other):
    return Or(self, other)
  def __repr__(self):
    return ("%s%s" % (type(self).__name__, self.items)).replace(",)",')')
  def __and__(self, other):
    return AndOr(self, other)
  return type(name, (), {'__init__':__init__, '__repr__':__repr__, '__or__':__or__, '__and__':__and__})


class Rule(str, tree_type("ruleo")):
  def __str__(self):
    return "Rule({0})".format(str.__str__(self))
  def __repr__(self):
    return "Rule({0})".format(str.__repr__(self))

Optional = tree_type("Optional")
Repeated = tree_type("Repeated")
Paren = tree_type("Paren")
Elidable = tree_type("Elidable")
Terminal = tree_type("Terminal")
Or = tree_type("Or")
AndOr = tree_type("AndOr")

REPEATED = MAGIC_ADD(Repeated)


if __name__ == '__main__':


  rules = {}
  terminals = {}

  parse(src)

  stdout.seek(0)
  s = orig = stdout.read()
  while '  ' in s:
      s = s.replace('  ', ' ')

  s = s.replace(" , ", ', ')
  s = s.replace(',,', ',')
  s = s.replace(', |, ', ' | ').replace(', &', ' & ').replace(", ^REPEATED", "^REPEATED")
  while '  ' in s:
      s = s.replace('  ', ' ')

  s = s.replace("& , ", '& ').replace("| , ", '| ')
  s = s.replace(',,', ',')
  s = s.replace(", +REPEATED", "+REPEATED")





  #print src
  #print s
  exec(s)
  if '--remake' in sys.argv:
    #The codee commented out below tries to re-make the EBNF from the structure
    #I don't think it really works. Blah, blah, bah.
    def to_bnf(grams):
      #Convert a rule to something that looks like BNF
      r = ''
      if type(grams) != tuple:
        grams = grams.items
      for sym in grams:
        t = type(sym)
        if t == Optional:
          r += '['+to_bnf(sym)+']'
        elif t == Repeated:
          r += to_bnf(sym)+'...'
        elif t == Paren:
          r += '('+to_bnf(sym)+')'
        elif t == Elidable:
          r += '/' + to_bnf(sym) + '/'
        elif t == Rule:
          r += sym.items[0]
        elif t == Or:
          r += to_bnf(sym.items[0])+'|'+to_bnf(sym.items[1])
        elif t == AndOr:
          r += to_bnf(sym.items[0])+'&'+to_bnf(sym.items[1])
        elif t == str:
          r += sym
        else:
          raise Exception("What with %s, %s" % (sym, type(sym)))
        r += ' '
      return r.strip()

    for k in rules:
      print(k, "=\n   ", end='')
      for g in rules[k]:
        print(to_bnf(g), end='')
      print(';')
  else:

    print("# -*- coding: utf-8 -*-")
    print()
    print("# generated on", time.asctime(), "by", os.popen('whoami').read().strip()+'@'+os.popen('hostname').read().strip())
    print()
    print("from bnfgen import *")
    print()
    print("rules = {")
    for k in rules:
      print("  Rule(%r)" %k, ':\n    ', rules[k], ',\\')
    print("}")
