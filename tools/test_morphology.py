#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
r = os.system('cat data/lujvo | ./morphology.py | grep "FUHIVLA\|SELBRI\|CMAVO\|CMENE\|GARBAGE"')
r += os.system('cat data/fuhivla | ./morphology.py | grep "LUJVO\|SELBRI\|CMAVO\|CMENE\|GARBAGE"')


