#!/usr/bin/python3.0
# -*- coding: utf-8 -*-

#thaumatology - handles (in the CLL's words) filtering, termination, and absorbtion
#For reference, see http://www.lojban.org/tiki/Magic+Words
# XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX
# XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX
# XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX
#     In need of a thorough investigation
# XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX
# XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX
# XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX

#Don't read, http://www.lojban.org/tiki/Magic+Words+Alternatives it is full of darkness and evil and LIES.

import sys, io

import config
from common import Buffer
import selmaho
import tokens

import morphology

class InterestStream:
  """
  Does pre-processing for the magic bits.
  <token> BU is
  XXX TODO Thought - Make this a Buffer object instead!
  """
  def __init__(self, valsi_iter, conf):
    self.valsi = valsi_iter
    self.config = conf

  def __iter__(self):
    while 1:
      while isinstance(self.valsi[0], tokens.IGNORABLE):
        self.valsi.pop()
      yield self.valsi.pop()

class QuoteStream:
  #It seems like QuoteParser handles things that go to the right, and ErasureParser handles things that go to the left
  def __init__(self, valsi_iter, conf):
    self.valsi = valsi_iter
    self.config = conf
  
  def __iter__(self):
    while 1:
      if self.valsi[0].type == selmaho.ZOI: #Non-lojban qiuote
        if self.config.raw_zoi:
          #XXX TODO ATM, doesn't work, very hacky too
          print("filter status", self.config.filter_zoi)
          stdin = self.config.stdin
          self.config.stdin = io.StringIO("")
          
            
          zoi = self.valsi.pop()
          delim = self.valsi.pop()
          targets = '.'+delim.value, ' '+delim.value
          if delim.type in (selmaho.SI, selmaho.SA, selmaho.SU):
            self.config.warn("{0!r} is a strange choice for a zoi deliminator".format(delim.value), delim.position)
          quote = ''
          while 1:
            if stdin:
              c = stdin.read(1)
            else:
              chars = self.config.glyph_table.get_char(self.config)
              c = ''
              for _ in chars: c += _.value

            if c == '':
              print(quote, ':', c)
              self.config.error("End of File reached in open ZOI quote (close it off with {0!r})".format(delim.value), delim.position)
            quote += c 
            for target in targets:
              if target and quote.endswith(target):
                break
              target = False
            if target:
              quote = quote[:-len(target)]
              self.config.debug("Found deliminator for ZOI, the quote is "+repr(quote),)
              break

          self.config.stdin = stdin
          zoi.content = quote.strip()
          yield zoi
        else: #Non-raw zoi, much easier, but the content is looked at by the morphology parser
          zoi = self.valsi.pop()
          delim = self.valsi.pop()
          while self.valsi[0].value != delim.value:
            try:
              zoi.value.append(self.valsi.pop())
            except:
              self.config.error("End of File reached in open ZOI quote (close it off with {0!r})".format(delim.value), delim.position)
          yield zoi
      elif self.valsi[0].type == selmaho.ZO: #1-word quote
        zo = self.valsi.pop()
        zo.content = self.valsi.pop()
        yield zo
      elif self.valsi[0].type == selmaho.LOhU: #Error quote
        lohu = self.valsi.pop()
        jbo_tokens = []
        while 1:
          try:
            vla = self.valsi.pop()
          except EOFError:
            self.config.error("End of File reached in open LOhU quote (end it with le'u) ", lohu.position)

          if vla.type == selmaho.LEhU:
            lehu = vla
            break
          jbo_tokens.append(vla)
        lohu.content = jbo_tokens
        #lohu.end = end_delim -- Nope, the LEhU is a seperate token
        yield lohu
        yield lehu
      else:
        yield self.valsi.pop()
        

"""
    self.si_depth = 5 #Store always at least 5 words for si erasure
    self.handle_su = True #Don't flush until EOT in case we find a su
    self.handle_sa = True #Don't flush for a sentence?
    self.flush_on = None #I or NIhO?
    self.end_on_faho = True #Treat FAhO as EOT, or uhm... don't yield it...?
"""

class ErasureStream:
  def __init__(self, valsi_iter, conf):
    self.valsi = valsi_iter
    self.config = conf
  def blank_iter(self):
    for v in self.valsi:
      yield v
  def __iter__(self):
    '''For sa: we only need to keep N of each selmaho, where N is how many repeated sa are permited
    For si: we only need to keep N valsi, where N is how many repeated si are permited
    For UI, we need to keep at least 1 valsi'''
    #XXX check for compliance with http://www.lojban.org/tiki/BPFK+Section:+Erasures&fullscreen=y
    #XXX Starting with full erasure handling, so TODO: limit erasure backlog...
    backlog = []
    stuff_behind = False #XXX TODO ????? Make exception if we can no longer erase old things
    while 1:
      try:
        self.valsi[0]
      except EOFError:
        self.EOF = True
        break
      
      if isinstance(self.valsi[0], tokens.HESITATION):
        # XXX NOTE XXX http://dag.github.com/cll/21/1/ says this should be handled AFTER si/sa/su, BUT nobody likes that.
        #{do .yyy si mi} would be {do mi}
        backlog[-1].modifiers.append(self.valsi.pop()) #If converting to set: use .add()
      elif self.valsi[0].type == selmaho.SI:
        #I agree with camxes, it should be ((zo si) si), not jbofihe's (zo (si si) si). It also says so in the CLL, http://dag.github.com/cll/21/1/
        #(BPFK seems silent on the issue)
        #(I suppose I could make a CLI option. jbofihe's way would be more work too)
        si = self.valsi.pop()
        if backlog:
          backlog.pop(-1)
      elif self.valsi[0].type == selmaho.SA:
        #CLL says, "as far back as until what follows attatches to what proceeds".
        #BPFK says to go back to the same selmaho
        sa = self.valsi.pop()
        count_back = 0 #How many target_type's to erase to
        #for example, {mi tavla tavla sa sa prenu}
        try:
          orig = sa
          while orig.type == selmaho.SA:
            orig = self.valsi.pop()
            count_back += 1
        except EOFError:
          self.config.error("EOT when trying to find match for SA", orig.position)
          backlog = []
          break
        target_type = orig.type
        if isinstance(orig, tokens.SELBRI):
          target_type = tokens.SELBRI
        found = False
        while 1:
          if not backlog:
            self.config.message("No backlog for SA")
            break
          b = backlog.pop(-1)
          if b.type == target_type or (isinstance(b, tokens.SELBRI) and target_type == tokens.SELBRI):
            count_back -= 1
            if count_back == 0:
              found = True
              break
        if not found and stuff_behind:
          self.config.error("Erasure buffer is not large enough for this SA", sa.position)
        if orig:
          backlog.append(orig)
      elif self.valsi[0].type == selmaho.SU:
        # XXX XXX TODO '"su" erases back to the previous word of selma'o NIhO, LU, TUhE, or TO'
        #Which this doesn't do properly
        su = self.valsi.pop()
        if not self.config.handle_su:
          self.config.error("SU are not enabled", su.position)
        else:
          backlog = []
      elif self.valsi[0].type == selmaho.ZEI:
        zei = self.valsi.pop(0)
        s1 = backlog.pop(0)
        s2 = self.valsi.pop(0)
        zei.content = [s1, s2]
        zei.type = tokens.SELBRI
        backlog.append(zei)
      elif self.valsi[0].type == selmaho.BU:
        bu = self.valsi.pop(0)
        if not bu.content:
          bu.content = backlog.pop()
        backlog.append(bu)
      else:
        # XXX TODO Here is where you would release some ammount of backlog, either "before the I" or "keep at least 5 words" or "per each NIhO" or something
        backlog.append(self.valsi.pop())
    for b in backlog:
      yield b

class AbsorptionStream:
  def __init__(self, valsi, conf):
    self.valsi = valsi
    self.conf = conf
  
  def __iter__(self):
    while 1:
      word = self.valsi.pop()
      if word.type == selmaho.FAhO:
        break
      next = self.valsi[0]
      #Ignore ZEI in http://dag.github.com/cll/21/1/
      if word.type == selmaho.BAhE:
        next.modifiers.append(word)
      else:
        while 1:
          if next.type == selmaho.UI:
            word.emphasis.append(self.valsi.pop())
          elif next.type in (selmaho.CAI, selmaho.NAI):
            if word.emphasis[-1].type == selmaho.UI:
              word.emphasis[-1].emphasis.append(self.valsi.pop())
            else:
              self.config.warn("Some may think differently, but IMHO having a CAI/NAI when there isn't a UI in front is weird.", next.position) #Well, okay, CAI I can see. But NAI? C'mon.
              word.emphasis.append(self.valsi.pop())
          elif next.type in (selmaho.DAhO, selmaho.FUhE, selmaho.FUhO):
            word.emphasis.append(self.valsi.pop())
          else:
            break
          next = self.vasli[0]
      
      yield word


def Stream(conf=None):
  if conf == None:
    conf = config.Configuration()
  
  
  valsi = morphology.Stream(conf=conf)
  interest = InterestStream(Buffer(valsi, conf), conf)
  quoted = QuoteStream(Buffer(interest, conf), conf)
  erased = ErasureStream(Buffer(quoted, conf), conf)
  absorbed = AbsorptionStream(Buffer(erased, conf), conf)
  return Buffer(absorbed, conf)

if __name__ == '__main__':
  results = []
  for _ in Stream(config.Configuration()):
    print(_, end=' ')
    #print(_.value, end=' ') # XXX Set this one for the release version, use above if in debug mode
    results.append(_)
  print()
