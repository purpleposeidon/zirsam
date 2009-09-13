#!/usr/bin/python3.0
# -*- coding: utf-8 -*-



def Rule(name, **grammar_rules):
  r = type(name, (Grammar,), original_grammar=grammar_rules)
  RULES[name] = r

RULES = {}

"""
How to Create a Rule
It is in this form:
  Rule("rule_name", SELMAhO="action", ... , WORD_TYPE="action", ... )
An action calls either a another rule, or (a SELMAhO or a WORD_TYPE).
It can be in four forms:
  "next_rule"
  "eat_token_to_variable next_rule"
  "<special>"
  ''
If it is in the first form, the current rule does not take the token. If it is in the second form, the token
is saved to the variable.
In the third form, a specific bit of code is used. Here is what is available:
  <terminate>
  <seperate>
When the rule is empty, the SELMAhO is used as the rule-name
If the rule ends in an ^, the rule is run only once. Otherwise, it is run so long as it has stuff to match.
"""
"""
Sorry. This doesn't quite make it.
I need to be able to say, [This, follows, that]
The THINGIE=equals is good. But it needs MOAR...
SELBRI CO SELBRI -> CO(SELBRI, SELBRI)
Ahhh..... right....
Okay, so, that "def" idea is a good idea because then you don't have to worry about referencing...
"""





#BEGIN RULES
Rule("document", other="section^", VAU='<terminate>')
Rule("section", NIhO="", other="sentence")
Rule("sentence", I="<seperate>", sumti="bridi_holder", selbri="bridi_holder", DOI="vocative")
Rule("bridi_holder", sumti='', selbri='selbri_bracket', CU="cu selbri_bracket")
Rule("vocative", COI='vocative_method', CMENE='')
Rule("sumti", LA="sumti_start CMENE", LE="sumti_start selbri_bracket", NU="abstractor")
#XXX Todo: What is sumti_start really called?
Rule("selbri_bracket", other="selbrilet")
Rule("selbrilet", CO="have_co selbrilet", SELBRI='')
Rule("structure_conversion", SE='')
Rule("abstractor", other="selbri_bracket^" KEI="<terminate>")
#END RULES


class Grammar():
  def __init__(self):
    self.terminal = []
  @staticmethod
  def evaluate_rulecase(r):
    if r.replace('h', 'H') == r.upper():
      if r == 'CMENE':
        return CMENE
      if r == 'SELBRI':
        return SELBRI
      if r == 'CMAVO':
        return CMAVO
      return selmahos[r]
    else:
      #It's a rule
      return RULES[r]
  def put_value(self, name, value):
    if not hasattr(self, name):
      setattr(self, name, [])
    getattr(self, name).append(value)
  def handle_action(self, parent, action):
    if action == '<terminate>':
      self.put_value("terminal", token_buffer.pop(0))
      return False
    if action == '<seperate>':
      return True
    if action == '':
      action = token_buffer[0].get_type()
    if ' ' in action:
      eat_to, action = action.split(' ')
      self.put_value(eat_to, token_buffer.pop(0))
    while 1:
      #child is either a Grammar(Rule) instance or a Selmaho(UI) instance
      child = self.evaluate_rulecase(action)()
      good_child = child.send(token_buffer)
      if good_child:
        self.put_value(action, child)
      if good_child != "CONTINUE":
        break
    return good_child
  def action_wrapper(self, parent, action):
    #Takes care of continuing rules
    if '^' in action:
      action = action.replace('^', '')
      loop = False
    else:
      loop = True

    while handle_action(parent, action):
      if not loop: break

  def send(self, parent, token_buffer):
    #Return True if we took it
    t_type = token_buffer[0].get_type()
    if t_type in self.grammar:
      return self.action_wrapper(parent, self.grammar[t_type]) #NodeType
    elif 'other' in self.grammar:
      return self.action_wrapper(parent, self.grammar['any'])
    return False



def Evaluate(token_buffer):
  return RULES["document"].send(token_buffer)








'''

def Setup_Rules():
What do you want?
RULES is in the form
"name" RuleType
We want to make it
name  RuleType?
??? No. wait. uhm. whuaaahhh.....
NO.
NONONO.
RULES is fine.
What we need to do is adjust
RuleType.
So....
Each RuleType has a dictionary, like
"selmaho or rule" into (selmaho or rule)
Okay. Uhm.
Why a dictionary? Why nott... Okay. I see. Ish.
So what we want to do is
Rule.Grammar[Token.Get_Type()]
THis way, we can easily figure out. Oh. So, actually, we WANT IT to stay a string! Goodness. Then.
Alright then.


  new_rules = []
  for rule_type in RULES:
    new_rules[rule_type] = None
  for rule in new_rules:
    #The keys in original_grammar are strings. We need to turn these into python objects
    new_grammar = {}
    for g in rule.original_grammar:
      if g.replace('h', 'H') == g.upper():
        #It's all in upper case letters, which means it's a real python variable
        new_grammar[eval(g)] = rule.original_grammar[g]
      else:
        #It's in lower case, meaning it's another rule
        new_grammar[RULES[g]] = rule.original_grammar[g]
    #Now that we have actual values for the dictionary, we simply add the new rule
    rule.grammar = new_grammar
'''




