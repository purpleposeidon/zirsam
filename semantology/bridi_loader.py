# -*- coding: utf-8 -*-


import tokens
import selmaho

fa2se = {1:'', 2:'se ', 3:'te ', 4:'ve ', 5:'xe '}


class Abstractlet:
  def __repr__(self):
    return "fi'o se {0} #{1}".format(self.bai, self.ma)
  def __init__(self, bai, ma):
    self.bai = bai
    self.ma = ma

class AbstractionExtractor:
  def __init__(self, config=None):
    self.abstractions = []
    self.da_count = 0
    self.config = config
    self.koha = {}
  def __repr__(self):
    return "ni'o "+' .i '.join(str(_) for _ in self.abstractions)
  def run(self, tracker):
    for sentence in tracker.search("sentence"):
      self.handle_sentence(sentence)
  def handle_term(self, tracker, fa_index, selbri):
    """
    Return an Abstractlet.
    TODO: Don't ignore FA
    """
    s6 = tracker.pull("sumti", "sumti_1", "sumti_2", "sumti_3", 'sumti_4', 'sumti_5', 'sumti_6')
    lo_zasti = self.da()
    if s6.node.get("LE"):
      le_selbri_node = s6.node["sumti_tail"].node["sumti_tail_1"].node["selbri"] #XXX .pull()?
      le_selbri = self.handle_selbri(le_selbri_node)
      self.abstractions.append(Abstractlet(le_selbri, lo_zasti))
    elif s6.node.get("KOhA"):
      self.abstractions.append(Abstractlet("<is "+s6.node.get("KOhA").value+">", lo_zasti))
    else:
      raise Exception()
    se_selbri = fa2se[fa_index]+selbri
    self.abstractions.append(Abstractlet(se_selbri, lo_zasti))
    return lo_zasti
    
  def da(self):
    self.da_count += 1
    return self.da_count
  def handle_selbri(self, tracker):
    """
    Return some kind of selbri item...A string for now I guess.
    TODO: Don't ignore SE
    """
    return list(tracker.search("tanru_unit_2"))[0].value[0].value


  def handle_sentence(self, tracker):
    """
    What do do here....
    Go through each sentence
    Extract the sumti
    """
    selbri_node = tracker.pull("bridi_tail", "bridi_tail_1", "bridi_tail_2", "bridi_tail_3", "selbri") #"
    selbri_type = self.handle_selbri(selbri_node)
    sumti_count = 0
    for term in tracker.search("term"):
      sumti_count += 1
      self.handle_term(term, sumti_count, selbri_type)



