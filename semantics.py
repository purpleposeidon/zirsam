#!/usr/bin/python
# -*- coding: utf-8 -*-
;  -*- coding: utf-8 -*-

"""
Okay, so...
Is this really the level it's at?

Maybe what I'm at is a step below this, the SELMAhO phase?
The cmavo all need to be classified.


"""



#base class for nodes...
class Node:
  def __init__(self, token_iter, config):
    self.tokens = token_iter
    self.config = config

  def handle_token(token):
    """
    
    """
    


'''
List of changes:
  Commented informational lines with ";"
  Replaced "= \n" with "= "
  Replaced "\n |" with " |"

'''
grammar = r"""
;  Lojban Machine Grammar, EBNF Version, 3rd Baseline as of 10 January 1997 
; This document is explicitly dedicated to the public domain by its author, the Logical Language Group Inc. Contact that organization at: 2904 Beau Lane, Fairfax VA 22031 USA 703-385-0273 (intl: +1 703 385 0273)
; Explanation of notation: All rules have the form:
;  namenumber = bnf-expression 
;  which means that the grammatical construct ``name'' is defined by ``bnf-expression''. The number cross-references this grammar with the rule numbers in the YACC grammar. The names are the same as those in the YACC grammar, except that subrules are labeled with A, B, C, ... in the YACC grammar and with 1, 2, 3, ... in this grammar. In addition, rule 971 is ``simple_tag'' in the YACC grammar but ``stag'' in this grammar, because of its frequent appearance. 
; Names in lower case are grammatical constructs.
; Names in UPPER CASE are selma'o (lexeme) names, and are terminals.
; Concatenation is expressed by juxtaposition with no operator symbol.
; | represents alternation (choice).
; [] represents an optional element.
; & represents and/or (``A & B'' is the same as ``A | B | A B'').
; ... represents optional repetition of the construct to the left. Left-grouping is implied; right-grouping is shown by explicit self-referential recursion with no ``...''
; () serves to indicate the grouping of the other operators. Otherwise, ``...'' binds closer than &, which binds closer than |.
; # is shorthand for ``[free ...]'', a construct which appears in many places.
; // encloses an elidable terminator, which may be omitted (without change of meaning) if no grammatical ambiguity results.
text0 = [NAI ...] [CMENE ... # | (indicators & free ...)] [joik-jek] text-1 
text-12 = [(I [jek | joik] [[stag] BO] #) ... | NIhO ... #] [paragraphs] 
paragraphs4 = paragraph [NIhO ... # paragraphs] 
paragraph10 = (statement | fragment) [I # [statement | fragment]] ... 
statement11 = statement-1 | prenex statement 
statement-112 = statement-2 [I joik-jek [statement-2]] ... 
statement-213 = statement-3 [I [jek | joik] [stag] BO # [statement-2]] 
statement-314 = sentence | [tag] TUhE # text-1 /TUhU#/ 
fragment20 = ek # | gihek # | quantifier | NA # | terms /VAU#/ | prenex | relative-clauses | links | linkargs 
prenex30 = terms ZOhU # 
sentence40 = [terms [CU #]] bridi-tail 
subsentence41 = sentence | prenex subsentence 
bridi-tail50 = bridi-tail-1 [gihek [stag] KE # bridi-tail /KEhE#/ tail-terms] 
bridi-tail-151 = bridi-tail-2 [gihek # bridi-tail-2 tail-terms] ... 
bridi-tail-252 = bridi-tail-3 [gihek [stag] BO # bridi-tail-2 tail-terms] 
bridi-tail-353 = selbri tail-terms | gek-sentence 
gek-sentence54 = gek subsentence gik subsentence tail-terms | [tag] KE # gek-sentence /KEhE#/ | NA # gek-sentence 
tail-terms71 = [terms] /VAU#/ 
terms80 = terms-1 ... 
terms-181 = terms-2 [PEhE # joik-jek terms-2] ... 
terms-282 = term [CEhE # term] ... 
term83 = sumti | (tag | FA #) (sumti | /KU#/) | termset | NA KU # 
termset85 = NUhI # gek terms /NUhU#/ gik terms /NUhU#/ | NUhI # terms /NUhU#/ 
sumti90 = sumti-1 [VUhO # relative-clauses] 
sumti-191 = sumti-2 [(ek | joik) [stag] KE # sumti /KEhE#/] 
sumti-292 = sumti-3 [joik-ek sumti-3] ... 
sumti-393 = sumti-4 [(ek | joik) [stag] BO # sumti-3] 
sumti-494 = sumti-5 | gek sumti gik sumti-4 
sumti-595 = [quantifier] sumti-6 [relative-clauses] | quantifier selbri /KU#/ [relative-clauses] 
sumti-697 = (LAhE # | NAhE BO #) [relative-clauses] sumti /LUhU#/ | KOhA # | lerfu-string /BOI#/ | LA # [relative-clauses] CMENE ... # | (LA | LE) # sumti-tail /KU#/ | LI # mex /LOhO#/ | ZO any-word # | LU text /LIhU#/ | LOhU any-word ... LEhU # | ZOI any-word anything any-word # 
sumti-tail111 = [sumti-6 [relative-clauses]] sumti-tail-1 | relative-clauses sumti-tail-1 
sumti-tail-1112 = [quantifier] selbri [relative-clauses] | quantifier sumti 
relative-clauses121 = relative-clause [ZIhE # relative-clause] ... 
relative-clause122 = GOI # term /GEhU#/ | NOI # subsentence /KUhO#/ 
selbri130 = [tag] selbri-1 
selbri-1131 = selbri-2 | NA # selbri 
selbri-2132 = selbri-3 [CO # selbri-2] 
selbri-3133 = selbri-4 ... 
selbri-4134 = selbri-5 [joik-jek selbri-5 | joik [stag] KE # selbri-3 /KEhE#/] ... 
selbri-5135 = selbri-6 [(jek | joik) [stag] BO # selbri-5] 
selbri-6136 = tanru-unit [BO # selbri-6] | [NAhE #] guhek selbri gik selbri-6 
tanru-unit150 = tanru-unit-1 [CEI # tanru-unit-1] ... 
tanru-unit-1151 = tanru-unit-2 [linkargs] 
tanru-unit-2152 = BRIVLA # | GOhA [RAhO] # | KE # selbri-3 /KEhE#/ | ME # sumti /MEhU#/ [MOI #] | (number | lerfu-string) MOI # | NUhA # mex-operator | SE # tanru-unit-2 | JAI # [tag] tanru-unit-2 | any-word (ZEI any-word) ... | NAhE # tanru-unit-2 | NU [NAI] # [joik-jek NU [NAI] #] ... subsentence /KEI#/ 
linkargs160 = BE # term [links] /BEhO#/ 
links161 = BEI # term [links] 
quantifier300 = number /BOI#/ | VEI # mex /VEhO#/ 
mex310 = mex-1 [operator mex-1] ... | FUhA # rp-expression 
mex-1311 = mex-2 [BIhE # operator mex-1] 
mex-2312 = operand | [PEhO #] operator mex-2 ... /KUhE#/ 
rp-expression330 = rp-operand rp-operand operator 
rp-operand332 = operand | rp-expression 
operator370 = operator-1 [joik-jek operator-1 | joik [stag] KE # operator /KEhE#/] ... 
operator-1371 = operator-2 | guhek operator-1 gik operator-2 | operator-2 (jek | joik) [stag] BO # operator-1 
operator-2372 = mex-operator | KE # operator /KEhE#/ 
mex-operator374 = SE # mex-operator | NAhE # mex-operator | MAhO # mex /TEhU#/ | NAhU # selbri /TEhU#/ | VUhU # 
operand381 = operand-1 [(ek | joik) [stag] KE # operand /KEhE#/] 
operand-1382 = operand-2 [joik-ek operand-2] ... 
operand-2383 = operand-3 [(ek | joik) [stag] BO # operand-2] 
operand-3385 = quantifier | lerfu-string /BOI#/ | NIhE # selbri /TEhU#/ | MOhE # sumti /TEhU#/ | JOhI # mex-2 ... /TEhU#/ | gek operand gik operand-3 | (LAhE # | NAhE BO #) operand /LUhU#/ 
number812 = PA [PA | lerfu-word] ... 
lerfu-string817 = lerfu-word [PA | lerfu-word] ... 
lerfu-word987 = BY | any-word BU | LAU lerfu-word | TEI lerfu-string FOI 
ek802 = [NA] [SE] A [NAI] 
gihek818 = [NA] [SE] GIhA [NAI] 
jek805 = [NA] [SE] JA [NAI] 
joik806 = [SE] JOI [NAI] | interval | GAhO interval GAhO 
interval932 = [SE] BIhI [NAI] 
joik-ek421 = joik # | ek # 
joik-jek422 = joik # | jek # 
gek807 = [SE] GA [NAI] # | joik GI # | stag gik 
guhek808 = [SE] GUhA [NAI] # 
gik816 = GI [NAI] # 
tag491 = tense-modal [joik-jek tense-modal] ... 
stag971 = simple-tense-modal [(jek | joik) simple-tense-modal] ... 
tense-modal815 = simple-tense-modal # | FIhO # selbri /FEhU#/ 
simple-tense-modal972 = [NAhE] [SE] BAI [NAI] [KI] | [NAhE] (time [space] | space [time]) & CAhA [KI] | KI | CUhE 
time1030 = ZI & time-offset ... & ZEhA [PU [NAI]] & interval-property ... 
time-offset1033 = PU [NAI] [ZI] 
space1040 = VA & space-offset ... & space-interval & (MOhI space-offset) 
space-offset1045 = FAhA [NAI] [VA] 
space-interval1046 = ((VEhA & VIhA) [FAhA [NAI]]) & space-int-props 
space-int-props1049 = (FEhE interval-property) ... 
interval-property1051 = number ROI [NAI] | TAhE [NAI] | ZAhO [NAI] 
free32 = SEI # [terms [CU #]] selbri /SEhU/ | SOI # sumti [sumti] /SEhU/ | vocative [relative-clauses] selbri [relative-clauses] /DOhU/ | vocative [relative-clauses] CMENE ... # [relative-clauses] /DOhU/ | vocative [sumti] /DOhU/ | (number | lerfu-string) MAI | TO text /TOI/ | XI # (number | lerfu-string) /BOI/ | XI # VEI # mex /VEhO/ 
vocative415 = (COI [NAI]) ... & DOI 
indicators411 = [FUhE] indicator ... 
indicator413 = (UI | CAI) [NAI] | Y | DAhO | FUhO

;  The following rules are non-formal:
word1100 = [BAhE] any-word [indicators]
any-word = ``any single word (no compound cmavo)''
anything = ``any text at all, whether Lojban or not'' 
null1101 = any-word SI | utterance SA | text SU
;  FAhO is a universal terminator and signals the end of parsable input. 
""".replace("#", "[free ...]")



'''
Superstructure

fa'o    ends text
i       seperates sentence
ni'o    seperates section/paragraphs/topics
  ni'o(volume)ni'o(story)ni'o(chapter) <stuff> ni'o(chapter) <stuff> ni'oni'o


DOM.ChildNode(this thing)
DOM.ParentNode()

Or, how about...
DOM.next()
DOM.down()
DOM.up()

DOM.next -> Adding another sumti
DOM.up   -> Setting the selbri
DOM.down -> Sub-item of current node

ni'o coi .djan. u'i fa'o
<text>
  <niho>
    <sentence>
      ni'o
      <vocative>
        coi
        <cmene "djan">
          <attitudinal "u'i">
        </cmene>
      </vocative>
    <sentence>
  </niho>
  fa'o
</text>


ni'o coi .djan. u'i .i do mo ta fa'o
<text>
  <niho>
    <sentence>
      ni'o
      <vocative>
        coi
        <cmene "djan">
          <attitudinal "u'i">
        </cmene>
      </vocative>
    <sentence>
    <sentence>
      <sumti>do</sumti>
      <selbri>mo</selbri>
      <sumti>ta</sumti>
    </sentence>
  </niho>
  fa'o
</text>


The current word means something to the word before it (Or some structure before it)
nu klama kei
cmavo(nu) means, "Make an abstraction node, add everything after that to this NU node"
selbri(klama) means, "Add me to the context's tanru unit"
cmavo(kei) means, "Close out the closest abstraction"

So, based on this example, then...
Each class of node can have some certain kind of sub-node.
For example, most every node has an attitudinal sub-node (I think...)

So, for a NU node...
  "Class KEI? I'll eat it, and send you up," and so we move to the node above, and feed that node the next token
  "Class CU? I've no idea," so we propagate up the tree.
For a SENTENCE node...
  "Class LE? I've got a list of sumti, I'll create a new SUMTI node, and feed that LE to it" (Let's pretend it's zo la)
    So zo la says, "Class CMENE? Perfect! I'm done now"
  "Class SELBRI? Well, I've got a nice tanru unit, I'll just feed you to it"
    So Mr. Tanru Unit says, "A SELBRI? Good, I'll add you in front of the list."
    "Another SELBRI? I'll put you in front of the list"
    "Oh, it's {co}, I'll make note to do some tanru inversion (And also to expect another selbri)"
    "Here's that other SELBRI I was expecting, we'll put it second in the list" (XXX Well. Uh, really, figure out what would be done?)
    "What's this? A LE? pitooie!"
  "What's this my tanru unit is giving me? A LE? Ah! {zo lo} This goes into my sumti-list..."
    "Alright, we're going to get a sumt-OF FUCK OH FUCK OH FUCK NO IT'S A SI SHITOSHITOSHITOSHIT, Uhh, okay, backup here...."
      #Maybe that don't work so well. Perhaps a "magic preprocessor" would be a good idea.
      We'd have a general handler take care of it.
      delete the last word (And, somehow, that word's effects. :/)
        Possibly have a delete(SELMA'O)
  "Well, gosh, that sucked. The next is a LE, {zo la}. Put it into my sumti-list..."
    "Fill me with your cmene!" And then it leaves immediatly, like a whore
  "Now I've got a LE, {zo le}. Another sumti-list"
    "You know what happens here. Of course, I keep checking for something that might apply to me. What's this? An {i}? Huh..."
  "What's that you've given me? An {i}? Oh, I guess my time here is up. Tah."
  
'''







