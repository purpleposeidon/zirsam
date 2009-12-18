#!/usr/bin/python3.0
# -*- coding: utf-8 -*-
#Slow as all hell, reuse this crap instead of calling bah
#Tests the grammar.... Oh boy!
import io
from subprocess import getstatusoutput as gso
import sys


camxes_cmd = "echo %r | java -Xss64m -jar /home/poseidon/Development/ideas/camxes/lojban_peg_parser.jar -t"
gso_fail = len(gso(camxes_cmd % (''))[1])



def compare_camxes(line):
  #Seems to work.
  res = gso(camxes_cmd % (line))[1]
  return res[gso_fail:] == line

def compare_jbofihe(line):
  return gso("echo %r | jbofihe" % (line))[0] == 0

def compare_zirsam(line):
  r = gso("echo %r | ~/sync/Development/JBOPARSER/dendrography.py --all-error" % line)[0]
  return r == 0

def run_line(line):
  if line.count('--') == 1:
    '''
    if '--' in line:
    #We've been told what we should expect
    if line.count('--') > 1:
      line = line[:line.find('--')].strip()
      '''
    try:
      line, expect = line.split('--')
    except Exception as e:
      print("Fuck.")
      print(e)
      return False
    expect = expect.strip()
    if expect == 'GOOD':
      expect = True
    elif expect == 'BAD':
      expect = False
    else:
      return run_line(line)
      #raise Exception
    a = compare_zirsam(line)
    if a != expect:
      print("\nzirsam:", a, "expected:", expect)
    return a == expect
  else:
    #First check with jbofihe, because it's faster.
    a = compare_zirsam(line)
    b = compare_jbofihe(line)
    if a != b:
      #Double-check with camxes, if zirsam disagrees with camxes then zirsam must be wrong
      c = compare_zirsam(line)
      if a != c:
        print("\nzirsam:", a, "jbofihe:", b, "camxes:", c, '\n')
        return False
    return True
        #return a == b
      #They match? Then jbofihe is wrong.
    



def run_test():
  IGNORE = []
  if 0:
    import io
    src = io.StringIO("""zomimi klama -- GOOD""")
  elif 0:
    src = open("data/gram_test_sentences.txt", errors='ignore')
    IGNORE = [6709] #Because jbofihe chokes up when it sees a paren
    print("This is going to take forever. Seriously. Like, a couple hours. Sorry.\n\n")
  else:
    src = open("data/failed_gram_tests.txt")
  i = 0
  failed_tests = 0
  for line in src:
    i += 1
    if i in IGNORE:
      failed_tests += 1
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
      failed_tests += 1
      #raise SystemExit
  print("Total tests:", i, "Failed tests:", failed_tests)
  print("Your grade for the course:", ((i-failed_tests)/i)*100)

if __name__ == '__main__':
  run_test()

