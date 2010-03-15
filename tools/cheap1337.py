#!/usr/bin/python3
import sys
##d = {'1':'pa', '2':'re', '3':'ci', '4':'vo', '5':'mu', '6':'xa', '7':'ze', '8':'bi', '9':'so', '0':'no'}
o = {'pa':'1', 're':'2', 'ci':'3', 'vo':'4', 'mu':'5', 'xa':'6', 'ze':'7', 'bi':'8', 'so':'9', 'no':'0'}
d = o
s = ''
while 1:
 try:
  c = sys.stdin.read(1)
  if c == '':
   break
  s += c
 except:
  break

for k, v in d.items():
 s = s.replace(k, v)
print(s)
