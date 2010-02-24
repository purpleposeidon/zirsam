#!/usr/bin/python3.0
# -*- coding: utf-8 -*-

import sys
import os
if os.path.basename(os.getcwd()) == 'semantology':
  os.chdir('../')
sys.path.append('./')


import config
import dendrography

import bridi_loader


#def main():
if 1:
  conf = config.Configuration()
  conf.parsing_unit = "x_parse_sentence"
  trackers = dendrography.Stream(conf)
  ae = bridi_loader.AbstractionExtractor(config=conf)
  for tracker in trackers:
    ae.run(tracker)
  #print("Life!")
  #print(repr(ae))
  print(ae)
  #print("Death! :(")


#if __name__ == '__main__':
  #c = main()
