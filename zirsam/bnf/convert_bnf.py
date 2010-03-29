#!/usr/bin/python3
# -*- coding: utf-8 -*-

#After you have put the *formal rules* of the CLL's BNF to data/lojban.bnf,
#run this program. It will utilize string handling and malmakfa to convert it
#into a python dictionary.
#Relacing and magic!

DISABLE_HASH = False #A little experiment

import re
import sys
import time, os
sys.path.append("./")

if __name__ != '__main__':
  raise ImportError("This is meant to be run as a script")


DATA_OUTPUT = "bnf_data.py"
date = time.asctime()
author = os.popen('whoami').read().strip()+'@'+os.popen('hostname').read().strip()

geninfo = "#automatically generated\n#on {0}".format(date)
if author:
  geninfo += "\n#by " + author

head_info = """#!/usr/bin/python3
# -*- coding: utf-8 -*-

{0}

import sys; sys.path.append('../')
from zirsam.magic_bnf import *
import zirsam.tokens
from zirsam.tokens import *
from zirsam.selmaho import *
import zirsam.special_terminals
from zirsam.special_terminals import *


""".format(geninfo)
tail_info = """BNF['any_word'] = any_word()
#BNF['unmatched'] = 'unmatched'
if __name__ == '__main__':
  if len(sys.argv) > 1:
    for key in sys.argv[1:]:
      print (key, ":", BNF[key])
  else:
    print (BNF)
"""

#Painful. Why?
sys.stdout = open(DATA_OUTPUT, 'w')
bnf = ''
bnf = open('../data/lojban.bnf').read()
bnf += '\n'
bnf += open('../data/extensions.bnf').read()


### The Relacing Part

#bnf = re.sub(pattern, rep, bnf)

#Remove comments
bnf = re.sub(r"(?m)(\w*;.*?$)", '', bnf) #m == MULTILINE

''' ### This now dealt with in dehtml_bnf.py
#Get rid of the subscripts -- only 1 number at the end!
bnf = re.sub(r"([\w-]\d)\d*", r"\1", bnf) #foo-bar-123 -> foo-bar-1
'''
while '  ' in bnf: bnf = bnf.replace("  ", ' ') #Kill extra spaces
while ' \n' in bnf: bnf = bnf.replace(' \n', '\n')
while '\n\n' in bnf: bnf = bnf.replace('\n\n', '\n')
#sys.stderr.write(bnf.replace('\n', '\\n\n'))

bnf = re.sub(r"([\w\d-]*) =", r";\n\1 = ", bnf).strip(';') +';' #Add ; after rules and at the end
bnf = bnf.replace('\n', '') #destroy newlines!
bnf = bnf.replace(';', "\n") #Now put the newlines back!
bnf = bnf.replace('  ', ' ').replace('\n\n', '\n').strip() #Cleanup again


bnf = bnf.replace('#', " #").replace('  ', ' ') #Fix /foo#/ to be /foo #/
if DISABLE_HASH:
  bnf = bnf.replace('#', ' ').replace('  ', '')
else:
  bnf = bnf.replace('#', '[free...]') #expand the #


#Now get ready to make that space our new concat operator
bnf = bnf.replace(' | ', '|').replace(' & ', '&').replace(' = ', '=')
bnf = bnf.replace(' ...', '...') #... binds closest

bnf = bnf.replace('-', '_') #For python validity

#Now make real python

bnf = re.sub(r"([\w\d_]+)", r"Term(\1)", bnf) #Rule contents

bnf = re.sub(r"Term\(([a-z\d_]+)\)", r"Rule('\1')", bnf) #Rule contents
bnf = re.sub(r"Term\(([A-Zh]+)\)", r"Terminal(\1)", bnf) #Rule contents


bnf = re.sub(r"/(.*?)/", r"Elidable(\1)", bnf) #Fix // (There are no //'s inside of //)

bnf = bnf.replace('[', "Optional(").replace(']', ")") #Fix []



while ' \n' in bnf: bnf = bnf.replace(' \n', '\n')


"""
Now for the malmakfa: I have the python parser parse it for me!
  I just have to exploit the orders of operation, and then write classes to implement those ops

Some orders of operations, from strongest precedent, to lowest precedent:
  **
  *
  +
  <<
  ^  (Don't want to use)
  |  (Don't want to use)
  == (Only if I'm desperate)
"""

if 1:
  #This is where everything becomes absolutely illegible
  bnf = bnf.replace('...', '**"REPEAT"') #repeat
  if 1: #The BNF seems unable to make up its mind on this point? >_>
    bnf = bnf.replace('&', '*') #and/or
    bnf = bnf.replace(' ', '+') #concat
  else:
    bnf = bnf.replace(' ', '/') #concat
    bnf = bnf.replace('&', '-') #and/or

  bnf = bnf.replace('|', '<<') #alternation

#Format it to look like a dictionary
bnf = bnf.replace('\n', ';\n')
bnf = bnf.replace('=', ':  ')
bnf = '\n'+bnf
bnf = bnf.replace('\nTerm', '\n  Term')
bnf = bnf.replace('\n\n', '\n')
bnf = bnf.replace(';', ',')


print(head_info)
print("BNF = {", bnf, "}", sep='\n')
print(tail_info)
#This + magic_bnf.BnfObjectBase == easier than writing a bnf parser, right?
