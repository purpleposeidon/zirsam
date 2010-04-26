#!/usr/bin/python3.0
# -*- coding: utf-8 -*-

from distutils.core import setup
import os
import sys
import glob

version = open("VERSION").read().strip()
rz = "purpleposeidonSPAM".replace("SPAM", '@g''ma''il.com')

def import_bnf():
  """
  This function loads the bnf module, thus making sure that the bnf data has been generated
  """
  sys.path.append('./')
  start = os.getcwd()
  os.chdir("zirsam")
  assert 'bnf' in os.listdir('./')
  print("Converting bnf data to python")
  import bnf
  os.chdir(start)

import_bnf()

setup(
  name="zirsam",
  version=version,
  author="James Royston",
  author_email=rz,
  url="http://github.com/purpleposeidon/zirsam",
  description="Lojban Parsing System",
  
  packages=['zirsam', 'zirsam.bnf'],
  package_data={'zirsam':["data/*"]},
  scripts=['tools/zirsam'],
)
