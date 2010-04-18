#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import os
os.chdir("../zirsam")
print("Morphology test. If anything is printed to STDOUT, there was an error", file=sys.stderr)
print("Testing lujvo...", file=sys.stderr)
r = os.system('cat data/lujvo | ./morphology.py | grep "FUHIVLA\|SELBRI\|CMAVO\|CMENE\|GARBAGE"')

print("Testing fu'ivla...", file=sys.stderr)
r += os.system('cat data/fuhivla | ./morphology.py | grep "LUJVO\|SELBRI\|CMAVO\|CMENE\|GARBAGE"')


