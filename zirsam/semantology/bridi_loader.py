# -*- coding: utf-8 -*-


import tokens
import selmaho

fa2se = {1:'', 2:'se ', 3:'te ', 4:'ve ', 5:'xe '}


class Abstractlet:
  def __repr__(self):
    return "#{1} {0}".format(self.bai, self.ma)
  def __init__(self, bai, ma):
    self.bai = bai
    self.ma = ma

class AbstractionExtractor:
  def __init__(self, config=None):
    self.abstractions = []
    self.da_count = 0
    self.config = config
    self.koha = {}
    self.goha = {}
  def __repr__(self):
    return ""+' .i\n'.join(str(_) for _ in self.abstractions)
    #return "ni'o "+' .i '.join(str(_) for _ in self.abstractions)
  def run(self, tracker):
    for sentence in tracker.search("sentence"):
      self.handle_sentence(sentence)
  def get_koha(self, koha):
    if koha in self.koha:
      return self.koha[koha]
    else:
      z = self.da()
      self.koha[koha] = z
      return z
  def handle_term(self, tracker, fa_index, selbri):
    """
    Return an Abstractlet.
    TODO: Don't ignore FA
    """
    s6 = tracker.pull("sumti", "sumti_1", "sumti_2", "sumti_3", 'sumti_4', 'sumti_5', 'sumti_6')
    if s6.node.get("LE"):
      le_selbri_node = s6.node["sumti_tail"].node["sumti_tail_1"].node["selbri"] #XXX .pull()?
      le_selbri = self.handle_selbri(le_selbri_node)
      self.abstractions.append(Abstractlet(le_selbri, lo_zasti))
      lo_zasti = self.da()
    elif s6.node.get("KOhA"):
      lo_zasti = self.get_koha(s6.node.get("KOhA").value)
      #self.abstractions.append(Abstractlet("<is "+s6.node.get("KOhA").value+">", lo_zasti))
      pass
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
    selbri = list(tracker.search("tanru_unit_2"))[0].value[0]
    if selbri in selmaho.GOhA:
      #Don't add GOhA to list....
      if selbri.value in self.koha:
        selbri = self.koha[selbri.value]
    else:
      if "go'i" in self.koha:
        self.koha["go'e"] = self.koha["go'i"]
      self.koha["go'i"] = selbri
    return selbri.value


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



