#!/usr/bin/python3.0
import sys
d = {'pa':'1', 're':'2', 'ci':'3', 'vo':'4', 'mu':'5', 'xa':'6', 'ze':'7', 'bi':'8', 'so':'9', 'no':'0'}
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
