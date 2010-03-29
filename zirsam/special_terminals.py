# -*- coding: utf-8 -*-

import zirsam.bnf.magic_bnf

class any_word:
  def __repr__(self):
    return "special_terminals.any_word"
  def match(self, tracker):
    try:
      tracker.valsi[tracker.get_offset()]
    except:
      return zirsam.bnf.magic_bnf.NoMatch
    
    tracker.accept_terminal()
    tracker.current_valsi += 1
    return zirsam.bnf.magic_bnf.Match
