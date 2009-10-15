# -*- coding: utf-8 -*-


"""
Get our BNF stuff, generate it if it isn't there, or re-gen if it's old
"""

import os
import sys
import time
did_CD = False
try:
  os.chdir('bnf') #XXX - Do this more robustly
  did_CD = True
except:
  if not 'convert_bnf.py' in os.listdir('./'):
    raise SystemExit("Please run directly from the JBOPARSER directory")

deps = "../data/lojban.bnf ../data/bnf.html convert_bnf.py dehtml_bnf.py magic_bnf.py __init__.py".split()
final = "bnf_data.py"
final_time = os.stat(final).st_mtime

redo_html = False
needs_redo = False
try:
  for d in deps:
    if os.stat(d).st_mtime > final_time:
      print("Dependency %s has been modified since bnf_data.py was last updated"%(d), file=sys.stderr)
      raise Exception("Files modified")
      if d == '../data/bnf.html':
        redo_html = True
  #import bnf_data
except:
  needs_redo = True
  if redo_html or not 'lojban.bnf' in os.listdir('../data'):
    if 'w3m' in os.popen('which w3m').read().strip():
      print("Extracting lojban.bnf from bnf.html", file=sys.stderr)
      os.system("python ./dehtml_bnf.py")
    else:
      if redo_html:
        print("Warning: BNF HTML source was modified, but don't have w3m to dump it.", file=sys.stderr)
      else:
        raise Exception("Could not find w3m. This program must be run to extract the bnf from the CLL html. Or you can get lojban.bnf from somewhere else, and put it into data/.")
  print("Converting data/lojban.bnf", file=sys.stderr)
  os.system("./convert_bnf.py")

#os.chdir('../')
import sys
sys.path.append('')
try:
  import bnf_data
  BNF = bnf_data.BNF
except:
  raise SystemExit("Unable to load BNF data. Some possible causes: Not being run from the correct directory, bad regexp applied to lojban.bnf, missing lojban.bnf, incorrect syntax in lojban.bnf")
__all__ = ['BNF']

if needs_redo:
  print("lojban BNF sucessfuly loaded!", file=sys.stderr)

#if did_CD:
  