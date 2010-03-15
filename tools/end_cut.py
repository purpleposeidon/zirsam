#!/usr/bin/python3
# -*- coding: utf-8 -*-
#XXX TODO Make this actually work
#As opposed to not working at all
#Which I'm pretty sure it does
#'cause I fail at maths.

def _8bits2char(d):
  bits = list(d)
  assert len(bits) == 8
  i = 0
  while bits:
    if bits.pop(-1): #Or bits.pop(0) XXX
      i += 2**len(bits)
  i = 1
  while bits:
    i = i << (bits.pop())
  return bytes(chr(i), encoding='utf')


def compress(array):
  #array is a list-like, each element is between like 0 and 2**14
  r = b''
  bits = []
  for i in array:
    #Kill the first two bits...
    i = i >> 1 >> 1
    while i:
      bits.append(i & 1)
      i = i >> 1
    if len(bits) >= 8:
      append = bits[:8]
      del bits[:8]
      r += _8bits2char(append)
  return r
  
def char_to_bits(i):
  #i = ord(c)
  bits = []
  while i:
    bits.append(i&1)
    i = i >> 1
  return bits

def decompress(bytes):
  bits = []
  r = b''
  for c in bytes:
    bits += char_to_bits(c)
    if len(bits) >= 8:
      delt = bits[:8]
      del bits[:8]
      r += _8bits2char(delt)
  if bits:
    bits += [0]*(8-len(bits))
    r += _8bits2char(bits)
  return r
