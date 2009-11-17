#!/usr/bin/python3.0
# -*- coding: utf-8 -*-

#Tests the grammar.... Oh boy!
import io
from subprocess import getstatusoutput as gso
import sys


camxes_cmd = "echo %r | java -Xss64m -jar /home/poseidon/Development/ideas/camxes/lojban_peg_parser.jar -t"
gso_fail = len(gso(camxes_cmd % (''))[1])



def compare_camxes(line):
  #uh, wtf do I do here?
  res = gso(camxes_cmd % (line))[1]
  return res[gso_fail:] == line

def compare_jbofihe(line):
  return gso("echo %r | jbofihe" % (line))[0] == 0

def compare_zirsam(line):
  return gso("echo %r | ~/sync/Development/JBOPARSER/dendrography.py") == 0

def run_line(line):
  if '--' in line:
    line, expect = line.split(' --')
    expect = expect.strip()
    if expect == 'GOOD':
      expect = True
    elif expect == 'BAD':
      expect = False
    else:
      raise Exception
    a = compare_zirsam(line)
    if a != expect:
      print("\nzirsam:", a, "expected:", expect)
    return a == expect
  else:
    #camxes is too slow to start
    a = compare_zirsam(line)
    b = compare_jbofihe(line)
    if a != b:
      print("\nzirsam:", a, "jbofihe:", b)
    return a == b


IGNORE = []

def run_test():
  src = open("data/gram_test_sentences.txt")
  i = 0
  for line in src:
    i += 1
    if i in IGNORE:
      continue
    #sys.stdout.write(str(i))
    #
    print(i, end='\r')
    sys.stdout.flush()
    line = line.strip()
    if line and line[0] == '#':
      continue
    if not line:
      continue
    result = run_line(line)
    if not result:
      print(line)
      print(i)
      raise SystemExit

if __name__ == '__main__':
  run_test()

