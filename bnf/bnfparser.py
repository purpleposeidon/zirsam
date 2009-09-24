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

stdout = io.StringIO()
src = open('../data/lojban.bnf').read()



parse()