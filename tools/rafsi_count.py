#!/usr/bin/python3
# -*- coding: utf-8 -*-
import io, sys
sys.path.append('./')
import morphology, config, tokens
import time
import pickle


#This is where the file is saved to
out_file = '/tmp/rafsi_frequency.txt'

#Load irc log data
f_name = "/tmp/all_logs.txt"
lines = []
for line in open(f_name):
  if '*' in line:
    continue
  l = line[line.find(">")+1:]
  l = l.strip()
  lines.append(l)
  

#Parse each line
def add(rafs):
  if rafs in rafsi:
    rafsi[rafs] += 1
  else:
    rafsi[rafs] = 1

rafsi = {}
total = len(lines)
start = time.time()
i = 0
for line in lines:
  i += 1
  stdin = io.StringIO(line+'\n')
  conf = config.Configuration(stdin=stdin)
  try:
    tokens = list(morphology.Stream(conf))
  except Exception as e:
    print(e)
    continue
  for valsi in tokens:
    for ra in valsi.ve_lujvo_rafsi:
      add(ra)
  print(i, '/', total, end='\r')
end = time.time()
print("\aTook:", end - start, "seconds")

#Key by frequency, and remove invalid rafsi
r2g = pickle.load(open('data/r2g.pyk3', 'rb'))
real_rafsi = list(r2g.keys())

re_map = {}
for rafs in rafsi:
  if rafs not in real_rafsi:
    continue
  count = rafsi[rafs]
  if count in re_map:
    re_map[count].append(rafs)
  else:
    re_map[count] = [rafs]

#Sort, and print
counts = list(re_map.keys())
counts.sort()
counts.reverse()

OUT = open(out_file, 'w')

for count in counts:
  for ra in re_map[count]:
    print(ra, '\t', count, file=OUT)
