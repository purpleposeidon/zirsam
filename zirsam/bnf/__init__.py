# -*- coding: utf-8 -*-


"""
Get our BNF stuff, generate it if it isn't there, or re-gen if it's old
"""

import os
import sys
import time

import zirsam.magic_bnf as magic_bnf

ORIG_DIR = os.getcwd()
#We need the curdir to be zirsam/bnf. So...
os.chdir(os.path.dirname(__file__))

deps = "../data/lojban.bnf ../data/bnf.html ../data/extensions.bnf convert_bnf.py optimizer.py dehtml_bnf.py __init__.py".split()
final = "bnf_data.py"
try:
  final_time = os.stat(final).st_mtime
except:
  final_time = 0
redo_html = False
needs_redo = False
try:
  for d in deps:
    if os.stat(d).st_mtime > final_time:
      #print("Dependency %s has been modified since bnf_data.py was last updated"%(d), file=sys.stderr)
      raise Exception("Files modified")
      if d == '../data/bnf.html':
        redo_html = True
  #import bnf_data
except:
  needs_redo = True
  try:
    datadir = None
    datadir = os.listdir('../data')
  except OSError:
    needs_redo = False
    #Let's just ignore it then...
  
  if needs_redo:
    if redo_html or not 'lojban.bnf' in datadir:
      if 'w3m' in os.popen('which w3m').read().strip():
        #print("Extracting lojban.bnf from bnf.html", file=sys.stderr)
        os.system("python3 ./dehtml_bnf.py")
      else:
        if redo_html:
          print("Warning: BNF HTML source was modified, but don't have w3m to dump it.", file=sys.stderr)
        else:
          raise Exception("Could not find w3m. This program must be run to extract the bnf from the CLL html. Or you can get lojban.bnf from somewhere else, and put it into data/.")
    #print("Converting data/lojban.bnf", file=sys.stderr)

    os.system("./convert_bnf.py")
    #os.system("./optimizer.py")

#os.chdir('../')
import sys
sys.path.append('./')

class BnfWrapper:
  def __init__(self, b):
    self.b = b
  
  def __getitem__(self, val):
    if type(val) == str:
      val = val.replace('-', '_')
    return self.b[val]
  
  def keys(self):
    return self.b.keys()



try:
  import bnf_data
except Exception as e:
  print("Unable to load BNF data. Some possible causes: Not being run from the correct directory, bad regexp applied to lojban.bnf, missing lojban.bnf, incorrect syntax in lojban.bnf", file=sys.stderr)
  print (e)
  raise
#__all__ = ['BNF']

#print (dir(bnf_data))
#bnf_data.BNF
#magic_bnf.BNF

#magic_bnf.BNF = bnf_data.BNF

#BNF = BnfWrapper(bnf_data.BNF)
def choose(bnf_name):
  return BnfWrapper(bnf_data.BNF_LIST[bnf_name])
  
os.chdir(ORIG_DIR)
