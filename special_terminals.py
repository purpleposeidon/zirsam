# -*- coding: utf-8 -*-

import magic_bnf

class any_word:
  def match(self, tracker):
    try:
      tracker.valsi[tracker.get_offset()]
    except:
      return magic_bnf.NoMatch
    
    tracker.accept_terminal()
    tracker.current_valsi += 1
    return magic_bnf.Match
