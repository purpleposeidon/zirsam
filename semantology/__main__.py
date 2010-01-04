#!/usr/bin/python3.0
# -*- coding: utf-8 -*-

import sys; sys.path.append('./')

import config
import dendrography

import semantology




def main():
  conf = config.Configuration()
  conf.parsing_unit = "x_parse_sentence"
  sentences = dendrography.Stream(conf)

  context = semantology.Context()
  
  for sentence in sentences:
    semantology.examine(sentence, context)
    #print(sentence)
  print(context)



if __name__ == '__main__':
  main()
