#!/usr/bin/python3.0
# -*- coding: utf-8 -*-

import io

import common
import config
import tokens


class AhuStream:
  """
  Gets rid of whitespace and pauses
  """
  def __init__(self, valsi_iter, conf):
    self.valsi = valsi_iter
    self.config = conf
  
  def __iter__(self):
    while 1:
      t = self.valsi.pop()
      if not isinstance(t, tokens.IGNORABLE):
        yield t

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
        


def Stream(conf=None):
  if not conf:
    conf = config.Configuration()