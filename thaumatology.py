#!/usr/bin/python3.0
# -*- coding: utf-8 -*-

#thaumatology - handle si/su. The CLL calls this "filtering".
#For reference, see http://www.lojban.org/tiki/Magic+Words
# XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX
# XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX
# XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX
#     In need of a thorough investigation
# XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX
# XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX
# XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX


import sys, io

import config
from common import Buffer
import selmaho
import tokens

import morphology

class BoreFilter:
  """
  Does pre-processing for the magic bits.
  <token> BU is
  """
  def __init__(self, valsi_iter, conf):
    self.valsi = valsi_iter
    self.config = conf

  def kill_extra_boring(self):
    #Kill non-hesitations
    try:
      while isinstance(self.valsi[0], tokens.BORING) and self.valsi[0].type != tokens.HESITATION:
        self.valsi.pop()
    except EOFError:
      pass

  def __iter__(self):
    while 1:
      self.kill_extra_boring()
      val = self.valsi.pop()
      self.kill_extra_boring()
      if val.type == tokens.HESITATION:
        #if followed by BU, yield BU(Y)
        if self.valsi[0].type == selmaho.BU:
          bu = self.valsi.pop()
          bu.content = val
          yield bu
        #If there is an EOF on valsi[0], then it wasn't a BU so we don't care.
      else:
        if val.type == selmaho.BU:
          pass #Do additional BU handling later on
          #self.config.error("nothing for bu to attach to", val.position)
        else:
          try:
            if self.valsi[0] == selmaho.BU:
              bu = self.valsi.pop()
              bu.content = val
              continue
          except EOFError:
            pass
        yield val

  def __Yiter__(self):
    while 1:
      val = self.valsi.pop()
      #print('pop', val)
      if not isinstance(val, tokens.BORING):
        self.kill_extra_boring()
        #print("live", self.valsi[0])
        if val.type == selmaho.BU:
          self.config.error("nothing for bu to attach to", val.position)
        try:
          if self.valsi[0].type == selmaho.BU:
            bu = self.valsi.pop()
            bu.content = val
            yield bu
            continue
        except EOFError:
          pass
        yield val
      else:
        if isinstance(val, tokens.HESITATION):
          #uhhh.... wait.... {.y.bu} could be a problem
          self.kill_extra_boring()
          #while isinstance(self.valsi[0], tokens.BORING):
            #_ = self.valsi.pop(0)
            #if isinstance(_, tokens.HESITATION):
              ##Could also have {.y.y.bu}, so we'd want to use the last one
              #val = _
          if self.valsi[0].type == selmaho.BU:
            bu = self.valsi.pop()
            bu.content = val
            yield bu

  def __Xiter__(self):
    while 1:
      val = self.valsi.pop()
      try:
        if self.valsi[0].type == selmaho.BU:
          if not(isinstance(val, tokens.BORING)) or isinstance(val, tokens.HESITATION):
            #Is interesting or an ybu
            bu = self.valsi.pop(0)
            bu.content = val
            yield bu
            continue
      except EOFError:
        pass
      if not isinstance(val, tokens.BORING):
        if val.type == selmaho.BU:
          self.config.error("nothing for bu to attach to", val.position)
        yield val
      


class QuoteParser:
  #It seems like QuoteParser handles things that go to the right, and ErasureParser handles things that go to the left
  def __init__(self, valsi_iter, conf):
    self.valsi = valsi_iter
    self.config = conf
  
  def __iter__(self):
    while 1:
      if self.valsi[0].type == selmaho.ZOI: #Non-lojban qiuote
        print("filter status", self.config.filter_zoi)
        if self.config.filter_zoi:
          stdin = self.config.stdin
          self.config.stdin = io.StringIO("")
        else: stdin = None
          
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

        if stdin:
          self.config.stdin = stdin
        zoi.content = quote.strip()
        yield zoi
      elif self.valsi[0].type == selmaho.ZOI: #Non-lojban quote
        zoi = self.valsi.pop()
        delim = self.valsi.pop()
        if delim.type in (selmaho.SI, selmaho.SA, selmaho.SU):
          self.config.warn("{0!r} is a strange choice for a zoi deliminator".format(delim.value), delim.position)
        non_jbo_tokens = []
        end_delim = None
        #self.config.message("the ZOI implementation is bad", zoi.position)
        # XXX XXX XXX This ignores boring things! Fix it! Include everything! Lazy bum!
        # Use strings. Shouldn't go through the parser, should try to access the underlying
        # file object directly.
        quote = ''
        EOF = False
        while 1:
          print("total quoted text is", repr(quote))
          if EOF:
            self.config.error("End of File reached in open ZOI quote (close it off with %r)"%(delim.value), delim.position)
          try:
            c = self.config.stdin.read(1)
            if c == '':
              raise EOFError
          except EOFError:
            c = ''
            EOF = True
          if self.config.filter_zoi:
            raise Exception("alphabet conversion for zoi not implemented")
          else:
            pass
          print("got character", repr(c))
          quote += c
          if quote.endswith(delim.value):
            quote = quote[:-len(delim.value)]
            break
        
        '''
        while 1:
          try:
            vla = self.valsi.pop()
          except EOFError:
            break
          if vla.value == delim.value:
            end_delim = vla
            break
          non_jbo_tokens.append(vla)
        if not end_delim:
          self.config.error("End of File reached in open ZOI quote (close it off with %r)"%(delim.value), delim.position)
        else:
          zoi.content = non_jbo_tokens
          zoi.end = delim, end_delim
          zoi.end = delim
          yield zoi'''
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
          ##############elif vla.type == selmaho.ZOI:
            ##############self.config.warn("zoi are *NOT* to be handled inside LOhU", vla.position) #http://www.lojban.org/tiki/Magic+Words+Alternatives
            ###Let's ignore that resource
          jbo_tokens.append(vla)
        lohu.content = jbo_tokens
        #lohu.end = end_delim -- Nope, the LEhU is a seperate token
        yield lohu
        yield lehu
      else:
        try:
          if 0: # self.valsi[1].type == selmaho.ZEI: #two words-to-brivla
            s1 = self.valsi.pop()
            zei = self.valsi.pop()
            s2 = self.valsi.pop()
            #zei.content = [s1, s2]
            zei.value = [s1, s2]
            zei.type = tokens.SELBRI
            yield zei
          else:
            yield self.valsi.pop()
        except EOFError:
          yield self.valsi.pop()
        

"""
self.allow_erasure = True
    self.si_depth = 5 #Store always at least 5 words for si erasure
    self.handle_su = True #Don't flush until EOT in case we find a su
    self.handle_sa = True #Don't flush for a sentence?
    self.flush_on = None #I or NIhO?
    self.end_on_faho = True #Treat FAhO as EOT, or uhm... don't yield it...?
"""

class ErasureParser:
  def __init__(self, valsi_iter, conf):
    self.valsi = valsi_iter
    self.config = conf
    if not self.config.allow_erasure:
      self.__iter__ = self.blank_iter
  def blank_iter(self):
    for v in self.valsi:
      yield v
  def __iter__(self):
    '''For sa: we only need to keep N of each selmaho, where N is how many repeated sa are permited
    For si: we only need to keep N valsi, where N is how many repeated si are permited'''
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
      if self.valsi[0].type == selmaho.ZEI:
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
      elif self.valsi[0].type == selmaho.SI:
        #I agree with camxes, it should be ((zo si) si), not jbofihe's (zo (si si) si). It also says so in the CLL, http://dag.github.com/cll/21/1/
        #(I suppose I could make a CLI option. jbofihe's way would be more work too)
        si = self.valsi.pop()
        if backlog:
          backlog.pop(-1)
      elif self.valsi[0].type == selmaho.SA:
        #CLL says, "as far back as until what follows attatches to what proceeds".
        #BPFK says to go back to the same selmaho
        sa = self.valsi.pop()
        count_back = 0 #How many target_type's to erase to
        try:
          orig = sa
          while orig.type == selmaho.SA: #For {mi tavla tava sa sa prenu}
            orig = self.valsi.pop()
            count_back += 1
        except EOFError:
          backlog = []
          break
        target_type = orig.type
        if isinstance(orig, tokens.SELBRI):
          target_type = tokens.SELBRI
        found = False
        while backlog:
          b = backlog.pop(-1)
          if b.type == target_type:
            count_back -= 1
            if count_back == 0:
              found = True
              break
        if not found and stuff_behind:
          self.config.warn("not enough left for sa to eat", sa.position)
        if orig:
          backlog.append(orig)
      elif self.valsi[0].type == selmaho.SU:
        # XXX XXX '"su" erases back to the previous word of selma'o NIhO, LU, TUhE, or TO'
        #Which this doesn't do properly
        su = self.valsi.pop()
        if not self.config.handle_su:
          if self.config._strict:
            self.config.strict("SU are not enabled", su.position)
          else:
            self.config.warn("ignoring this SU!", su.position) #Probably messing up EVERYTHING...
        else:
          backlog = []
      else:
        backlog.append(self.valsi.pop())
      #print (backlog)
    for b in backlog:
      yield b

class FAhOParser:
  def __init__(self, valsi_iter, config):
    self.valsi = valsi_iter
    self.config = config

  def __iter__(self):
    for v in self.valsi:
      if v.type == selmaho.FAhO:
        if self.config.end_on_faho:
          break
        continue
      yield v

def Stream(conf=None):
  if conf == None:
    conf = config.Configuration()
  

  valsi_stream = morphology.Stream(conf=conf)
  interest_stream = Buffer(BoreFilter(valsi_stream, conf), conf)
  quote_stream = Buffer(QuoteParser(interest_stream, conf), conf)
  faho_stream = Buffer(FAhOParser(quote_stream, conf), conf)
  return Buffer(ErasureParser(faho_stream, conf), conf)
  #return Buffer(MagicParser(interest_stream, conf))

if __name__ == '__main__':
  results = []
  for _ in Stream(config.Configuration()):
    print(_, end=' ')
    #print(_.value, end=' ') # XXX Set this one for the release version, use above if in debug mode
    results.append(_)
