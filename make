#!/bin/sh
cd zirsam/bnf/
./convert_bnf.py
cd ..
cd ..
./setup.py build && sudo ./setup.py install
echo
echo
