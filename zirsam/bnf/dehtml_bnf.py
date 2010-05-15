#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import re
import os
import tempfile

bnf = open('../data/bnf.html').read()

bnf = bnf[bnf.find("<dl>")+4:bnf.find("</dl>")]

#out = os.tempnam()+'.html' #Not that you care
outFD, out = tempfile.mkstemp(suffix='.html')

open(out, 'w').write(bnf)

out2FD, out2 = tempfile.mkstemp() #Nor that you care here, either!

os.system("w3m -dump %s > %s" % (out, out2))
bnf = open(out2).read()

bnf = re.sub(r'\[\d*\]', '', bnf)

os.close(outFD); os.close(out2FD)
os.unlink(out)
os.unlink(out2)
while ' \n' in bnf:
  bnf = bnf.replace(' \n', '\n') #Agh! The trailing spaces! They BURN
open('../data/lojban.bnf', 'w').write(bnf)
###def kill_tag(a, bnf):
  ###return re.sub(r"<a.*?>".replace('a', a), '', bnf, re.S)

###bnf = re.sub(r"<a .*?>(.*)</a>", '\0', bnf, re.S)
###bnf = re.sub(r"<a .*?>", '', bnf, re.S)
####assert not '<a' in bnf
###bnf = re.sub(r"<sub>.*?</sub>", '', bnf, re.S)


#print (bnf)
#open('src_bnf.bnf', 'w').write(bnf)
