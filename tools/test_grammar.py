#!/usr/bin/python3
# -*- coding: utf-8 -*-
#Slow as all hell, reuse this crap instead of calling bah
#Tests the grammar.... Oh boy!
import io
import sys
from subprocess import getstatusoutput as gso

import zirsam
import zirsam.dendrography as dendrography
import zirsam.config as config

camxes_cmd = "echo %r | java -Xss64m -jar /home/poseidon/Development/ideas/camxes/lojban_peg_parser.jar -t"
gso_fail = len(gso(camxes_cmd % (''))[1])



def compare_camxes(line):
  #Seems to work.
  res = gso(camxes_cmd % (line))[1]
  return res[gso_fail:] == line

def compare_jbofihe(line):
  return gso("echo %r | jbofihe" % (line))[0] == 0

#def compare_zirsam(line):
  #r = gso("echo %r | ~/sync/Development/JBOPARSER/dendrography.py --all-error" % line)[0]
  #return r == 0

def compare_zirsam(line):
  s = dendrography.Stream(config.Configuration(stdin=io.StringIO(line), args=['--all-error', '--forbid-warn', '--no-exit'], stdout=io.StringIO(), stderr=io.StringIO()))
  try:
    l = len(list(s))
    if l == 0:
      #XXX Assuming that it is 0 because stuff was deleted
      return True
    return s.orig.good_parse and s.orig.config.perfect_parse
  except KeyboardInterrupt:
    raise SystemExit("Keyboard Interrupt")
  except:
    return False
  return val

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
      print("Bad line:", line, file=sys.stderr)
      print(e, file=sys.stderr)
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
      print("\nzirsam:", a, "expected:", expect, file=sys.stderr)
    return a == expect
  else:
    #First check with jbofihe, because it's faster.
    a = compare_zirsam(line)
    b = compare_jbofihe(line)
    if a != b:
      #Double-check with camxes, if zirsam disagrees with camxes then zirsam must be wrong
      c = compare_zirsam(line)
      if a != c:
        print("\nzirsam:", a, "jbofihe:", b, "camxes:", c, '\n', file=sys.stderr)
        return False
    return True
        #return a == b
      #They match? Then jbofihe is wrong.
    



def run_test():
  if '--help' in sys.argv:
    print("""Usage:
    ./tools/test_grammar.py [optional options]
      --help    show this message
      --test    Run a few test-lines
      --full    Run a complete and full check, takes extra long
      --use filename
                Use filename as the source for tests
    If given no options, will """, file=sys.stderr)
    raise SystemExit
  IGNORE = []
  if '--test' in sys.argv:
    src = io.StringIO("""zomimi klama -- GOOD\nbroda do brodi -- BAD""")
    #src = io.StringIO("""zomimi klama -- BAD\nbroda do brodi -- GOOD""")
  elif '--full' in sys.argv:
    src = open(zirsam.resource("gram_test_sentences.txt"), errors='ignore')
    IGNORE = [6709] #Because jbofihe chokes up and dies when it sees a paren
    print('*'*10, file=sys.stderr)
    print("This is going to take forever; like, a couple hours (1.5 on my machine). Sorry! (bnf optimizations, get pypy/cython going or something, but probably still isn't out for py3k)", file=sys.stderr)
    print('*'*10, file=sys.stderr)
  elif '--use' in sys.argv:
    src = open(sys.argv[sys.argv.index('--use')+1], errors='ignore')
  else:
    src = open(zirsam.resource('failed_gram_tests.txt'), errors='ignore')
  i = 0
  failed_tests = 0
  fail_lines = []
  f = input("Enter file to append errors to [/dev/null]: ")
  if f: failures = open(f, 'a')
  else: failures = open('/dev/null', 'w')
  for line in src:
    i += 1
    if i in IGNORE:
      #failed_tests += 1
      continue
    #sys.stdout.write(str(i))
    #
    print(i, end='\r', file=sys.stderr)
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
      fail_lines += line
      failures.write(line+'\n')
      #raise SystemExit
  failures.close()
  print("Total tests:", i, "Failed tests:", failed_tests, file=sys.stderr)
  print("Grade for the course:", ((i-failed_tests)/i)*100, file=sys.stderr)
  print("(Not that it means anything)", file=sys.stderr)
  

if __name__ == '__main__':
  run_test()

