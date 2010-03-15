#!/usr/bin/python3
# -*- coding: utf-8 -*-

from distutils.core import setup
import os, glob

import __init__

setup(
  name="zirsam",
  description="Lojban Parsing System",
  author="James Royston",
  author_email="purpleposeidon@gmail.com"
  url="http://github.com/purpleposeidon/zirsam"
  version=__init__.__version__,
  py_modules=['foo'],
  packages=['bnf'],
  package_data={'zirsam':["data/*"]},
)