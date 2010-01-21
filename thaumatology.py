#!/usr/bin/python3.0
# -*- coding: utf-8 -*-

#thaumatology - handles (in the CLL's words) filtering, termination, and absorbtion
#For reference, see http://www.lojban.org/tiki/Magic+Words
#That URL is assumed to refer to the canonical description for magic-word handling

#Don't read, http://www.lojban.org/tiki/Magic+Words+Alternatives it is full of darkness and evil and LIES.
#Don't make me repeat myself, don't click on the link!


import sys, io

import config
from common import Buffer
import selmaho
import tokens

import morphology

class InterestStream:
  """
  Does pre-processing for the magic bits.
  XXX TODO Thought - Make this a Buffer object instead!
  It doesn't do very much
  """
  def __init__(self, valsi_iter, conf):
    self.valsi = valsi_iter
    self.config = conf

  def __iter__(self):
    y = None
    while 1:
      boring = []
      while isinstance(self.valsi[0], tokens.IGNORABLE):
        boring.append(self.valsi.pop())
      v = self.valsi.pop()
      v.whitespace = boring
      boring = []
      if y:
        if v in selmaho.BU:
          v.content = y
          #Try this for fun: zo .y. fusi bu
        else:
          yield y
        y = None
      if isinstance(v, tokens.HESITATION):
        y = v
        continue
      yield v

class QuoteStream:
  #Especially things that go forwards
  def __init__(self, valsi_iter, conf):
    self.valsi = valsi_iter
    self.config = conf
  
  def __iter__(self):
    while 1:
      if self.valsi[0].type == selmaho.ZOI: #Non-lojban quote
        #TODO: It'd be nice to turn off warnings and messages from morphology in here
        #self.config.message("Start of a ZOI quote; all errors can be ignored.")
        
        zoi = self.valsi.pop()
        delim_start = self.valsi.pop()
        if delim_start.type in (selmaho.SI, selmaho.SA, selmaho.SU, selmaho.ZO, selmaho.BU, selmaho.ZEI, selmaho.FAhO):
          self.config.message("This ZOI deliminator (%r) could be confusing to the unenlightened" % (delim_start.value), delim_start.position)
        quote_tokens = []
        
        orig_stderr = self.config.stderr #Only hide errors inside the actual zoi quote, don't exclude errors
        self.config.stderr = io.StringIO() #involving the deliminator
        
        try:
          while self.valsi[0].value != delim_start.value:
            next = self.valsi.pop()
            quote_tokens.append(next)
        except (EOFError, StopIteration):
          self.config.stderr = orig_stderr
          self.config.error("End of File reached in open ZOI quote (close it off with {0!r})".format(delim_start.value), delim_start.position)
        delim_end = self.valsi.pop()
        zoi.end = delim_end
        zoi.start = delim_start
        zoi.zoi_tokens = quote_tokens
        self.config.stderr = orig_stderr
        
        start = delim_start.position.offset+len(delim_start.value)
        end = delim_end.position.offset-1
        
        if len(quote_tokens) >= 1:
          """
          How to trim the data...
          "zoi ", "zoi. ", "zoi."
          " zoi", " .zoi", ".zoi"
          """
          trim_space = 0
          trim_pause = False
          for token in zoi.zoi_tokens[0].whitespace:
            if isinstance(token, tokens.PERIOD):
              trim_pause = True
            if isinstance(token, tokens.WHITESPACE):
              trim_space += 1
            start = zoi.zoi_tokens[0].position.offset-1
          white = list(zoi.end.whitespace)
          
          white.reverse()
          for token in white:
            end = token.position.offset - 1
            if isinstance(token, tokens.PERIOD):
              if not trim_pause:
                break
              trim_pause = False
            elif isinstance(token, tokens.WHITESPACE):
              if trim_space == 0:
                break
              trim_space -= 1
        
        zoi.content = self.config.old_chars[start:end]
        yield zoi
      elif self.valsi[0].type == selmaho.ZO: #1-word quote
        zo = self.valsi.pop()
        try:
          zo.content = self.valsi.pop()
        except:
          self.config.warn("ZO should have something to be quoted", zo.position)
        yield zo
      elif self.valsi[0].type == selmaho.LOhU: #Error quote
        lohu = self.valsi.pop()
        jbo_tokens = []
        while 1:
          try:
            vla = self.valsi.pop()
            if vla.type == selmaho.ZOI:
              self.config.message("This implementation doesn't do ZOI in LOhU", vla.position)
          except EOFError:
            self.config.error("End of File reached in open LOhU quote (end it with le'u) ", lohu.position)

          if vla.type == selmaho.LEhU:
            lehu = vla
            break
          jbo_tokens.append(vla)
        lohu.content = jbo_tokens
        lohu.end = lehu #I'd rather yield lehu
        yield lohu
      elif self.valsi[0].type == selmaho.LEhU: #Erroneous error quote end
        lehu = self.valsi.pop()
        self.config.warn("Trying to close a non-existant error quote", lehu.position)
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
  #Especially things that go backwards
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
      
      #if isinstance(self.valsi[0], tokens.HESITATION):
        ## XXX NOTE XXX http://dag.github.com/cll/21/1/ says this should be handled AFTER si/sa/su, BUT nobody likes that. 
        ##{do .yyy si mi} would be {do mi}
        #y = self.valsi.pop()
        #try:
          #maybu = self.valsi[0].type == selmaho.BU
        #except (EOFError, IndexError):
          #maybu = False
        #if backlog and not maybu:
          #backlog[-1].modifiers.append(y) #If converting to set: use .add()
        #else:
          #backlog.append(y)
      #el
      if self.valsi[0].type == selmaho.SI:
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
        
        if isinstance(orig, tokens.BRIVLA):
          target_type = tokens.BRIVLA
        found = False
        LOHU_CASE = False #XXX I'm saying this at 2:54 am, check at some point please.
        while 1:
          if not backlog:
            self.config.message("No backlog for SA")
            break
          b = backlog.pop(-1)
          LOHU_CASE = (target_type == selmaho.LEhU and b.type == selmaho.LOhU)
          if b.type == target_type or (isinstance(b, tokens.BRIVLA) and target_type == tokens.BRIVLA) \
            or LOHU_CASE:
            count_back -= 1
            if count_back == 0:
              found = True
              if LOHU_CASE:
                b.end = orig
                backlog.append(b)
                self.config.message("This lojbanist thinks SA LEhU is stupid.")
              break
        if not found and stuff_behind:
          self.config.error("Erasure buffer is not large enough for this SA", sa.position)
        if orig and not LOHU_CASE:
          backlog.append(orig)
      elif self.valsi[0].type == selmaho.SU:
        su = self.valsi.pop()
        if not self.config.handle_su:
          self.config.error("SU are not enabled", su.position)
        else:
          su_stoppers = selmaho.NIhO, selmaho.LU, selmaho.TUhE, selmaho.TO
          while backlog:
            if backlog[-1].type in su_stoppers:
              #backlog.pop(-1) #Fixed: "I suppose they are supposed to be erased", but not according to camxes
              break
            backlog.pop(-1)
          if backlog == [] and stuff_behind:
            self.config.error("Erasure buffer is not large enough for this SU", su.position)
          #backlog = []
      elif self.valsi[0].type == selmaho.ZEI:
        zei = self.valsi.pop(0)
        try:
          s1 = backlog.pop(0)
        except IndexError:
          self.config.error("There is nothing for ZEI to bind on the left", zei.position)
        try:
          s2 = self.valsi.pop(0)
        except (StopIteration, EOFError):
          self.config.error("There is nothing for ZEI to bind on the right", zei.position)
        zei.content = [s1, s2]
        
        zei.type = tokens.LUJVO #The BNF uses ZEI, so it's just going unused.
        backlog.append(zei)
      elif self.valsi[0].type == selmaho.BU:
        bu = self.valsi.pop(0)
        if not bu.content:
          try:
            bu.content = backlog.pop()
          except (IndexError):
            self.config.warn("BU must have something to quote!", bu.position)
        if bu.content and bu.content.value == 'zei':
          self.config.message("You're going to hell if you actually use this", bu.position)
        #else: It should be .y.bu
        backlog.append(bu)
      else:
        # XXX TODO Here is where you would release some ammount of backlog, either "before the I" or "keep at least 5 words" or "per each NIhO" or something
        backlog.append(self.valsi.pop())
    for b in backlog:
      yield b

class AbsorptionStream:
  def __init__(self, valsi, conf):
    self.valsi = valsi
    self.config = conf
  
  def __iter__(self):
    word = None
    try:
      while 1:
        word = self.valsi.pop()
        if word.type == selmaho.FAhO:
          break
        
        #Ignore ZEI in http://dag.github.com/cll/21/1/
        try:
          if word.type == selmaho.BAhE:
            self.valsi[0].modifiers.append(word)
            continue
        except (StopIteration, EOFError):
          self.config.warn("BAhE has nothing to emphasize", word.position)
          
        next = self.valsi[0]
        while 1:
          """
          d. If selma'o NAI occurs immediately following any of tokens UI or CAI, absorb the NAI into the previous token.
          e. Absorb all members of selma'o DAhO, FUhO, FUhE, UI, Y, and CAI into the previous token. All of these null grammar tokens are permitted following any word of the grammar, without interfering with that word’s grammatical function, or causing any effect on the grammatical interpretation of any other token in the text. Indicators at the beginning of text are explicitly handled by the grammar.
          """
          if next.type in (selmaho.UI, selmaho.CAI):
            try:
              if self.valsi[1].type == selmaho.NAI:
                nai = self.valsi.pop(1)
                next.modifiers.append(nai)
                continue
            except (EOFError, StopIteration):
              pass
          if next.type in (selmaho.DAhO, selmaho.FUhO, selmaho.FUhE, selmaho.UI, selmaho.CAI) or isinstance(next, tokens.HESITATION):
            word.modifiers.append(self.valsi.pop())
            next = self.valsi[0]
          else:
            break
          
              
          '''
          #Possible cases:
          #valsi ui[nai]
          #valsi nai
          #ui[nai]
          #nai[ui]
          if next.type == selmaho.UI:
            word.modifiers.append(self.valsi.pop())
          elif next.type in (selmaho.CAI, selmaho.NAI):
            if word.modifiers[-1].type == selmaho.UI:
              word.modifiers[-1].modifiers.append(self.valsi.pop())
            else:
              self.config.warn("Some may think differently, but IMHO having a CAI/NAI when there isn't a UI in front is weird.", next.position) #Well, okay, CAI I can see. But NAI? C'mon.
              word.modifiers.append(self.valsi.pop())
          elif next.type in (selmaho.DAhO, selmaho.FUhE, selmaho.FUhO):
            word.modifiers.append(self.valsi.pop())
          else:
            break
          next = self.valsi[0]
          '''
        yield word
    except (EOFError, StopIteration):
      assert self.valsi.buffer == []
      if word:
        yield word

def Stream(conf=None):
  if conf == None:
    conf = config.Configuration()
  
  
  valsi = morphology.Stream(conf=conf)
  interest = InterestStream(Buffer(valsi, conf), conf)

  quoted = QuoteStream(Buffer(interest, conf), conf)
  
  erased = ErasureStream(Buffer(quoted, conf), conf)
  #return Buffer(erased, conf)
  absorbed = AbsorptionStream(Buffer(erased, conf), conf)
  if conf.show_progress:
    absorbed = list(absorbed)
    print("Total valsi:", len(absorbed))
  return Buffer(absorbed, conf)

if __name__ == '__main__':
  results = []
  for _ in Stream(config.Configuration()):
    print(_, end=' ')
    sys.stdout.flush()
    #print(_.value, end=' ') # XXX Set this one for the release version, use above if in debug mode
    results.append(_)
  print()
  r = results
