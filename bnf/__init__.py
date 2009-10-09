# -*- coding: utf-8 -*-


"""
Get our BNF stuff, generate it if it isn't there, or re-gen if it's old
"""

import os
import sys
import time

try:
  os.chdir('bnf') #XXX - Do this more robustly
except:
  if not 'convert_bnf.py' in os.listdir('./'):
    raise SystemExit("Please run directly from the JBOPARSER directory")

deps = "../data/lojban.bnf ../data/bnf.html convert_bnf.py dehtml_bnf.py magic_bnf.py".split()
final = "bnf_data.py"
final_time = os.stat(final).st_mtime


try:
  for d in deps:
    if os.stat(d).st_mtime > final_time:
      print ("Dependency %s has been modified since bnf_data.py was last updated"%(d), file=sys.stderr)
      raise Exception("Files modified")
  #import bnf_data
except:
  if not 'src_bnf.bnf' in os.listdir('./'):
    if 'w3m' in os.popen('which w3m').read().strip():
      sys.stderr.write("Cleaning up HTML BNF\n")
      os.system("python ./dehtml_bnf.py")
    else:
      print("Warning: BNF HTML source was modified, but don't have w3m to dump it.")
  sys.stderr.write("Converting data/lojban.bnf\n")
  os.system("python ./convert_bnf.py")
  #os.chdir('../')
import bnf_data

BNF = bnf_data.BNF
__all__ = ['BNF']
