# -*- coding: utf-8 -*-

"""
Ony defines the AnyWord class; nothing else is needed.
"""

import zirsam.magic_bnf

class AnyWord:
    """
    Matches a single token.
    """
    def __repr__(self):
        return "special_terminals.any_word"
    def match(self, tracker):
        """
        Return Match if there is a word.
        """
        try:
            tracker.valsi[tracker.get_offset()]
        except:
            return zirsam.magic_bnf.NoMatch
        
        tracker.accept_terminal()
        tracker.current_valsi += 1
        return zirsam.magic_bnf.Match
