#!/usr/bin/python3.0
# -*- coding: utf-8 -*-

#automatically generated
#on Sun Dec 13 20:27:59 2009
#by poseidon@skami

from magic_bnf import *
import sys; sys.path.append('../')
from tokens import *
from selmaho import *
from special_terminals import *

BNF = {

Rule('text'):  Optional(Terminal(NAI)**"REPEAT")*Optional(Terminal(CMENE)**"REPEAT"*Optional(Rule('free')**"REPEAT")<<(Rule('indicators')+Rule('free')**"REPEAT"))*Optional(Rule('joik_jek'))*Rule('text_1'),
Rule('text_1'):  Optional((Terminal(I)*Optional(Rule('jek')<<Rule('joik'))*Optional(Optional(Rule('stag'))*Terminal(BO))*Optional(Rule('free')**"REPEAT"))**"REPEAT"<<Terminal(NIhO)**"REPEAT"*Optional(Rule('free')**"REPEAT"))*Optional(Rule('paragraphs')),
Rule('paragraphs'):  Rule('paragraph')*Optional(Terminal(NIhO)**"REPEAT"*Optional(Rule('free')**"REPEAT")*Rule('paragraphs')),
Rule('paragraph'):  (Rule('statement')<<Rule('fragment'))*Optional(Terminal(I)*Optional(Rule('free')**"REPEAT")*Optional(Rule('statement')<<Rule('fragment')))**"REPEAT",
Rule('statement'):  Rule('statement_1')<<Rule('prenex')*Rule('statement'),
Rule('statement_1'):  Rule('statement_2')*Optional(Terminal(I)*Rule('joik_jek')*Optional(Rule('statement_2')))**"REPEAT",
Rule('statement_2'):  Rule('statement_3')*Optional(Terminal(I)*Optional(Rule('jek')<<Rule('joik'))*Optional(Rule('stag'))*Terminal(BO)*Optional(Rule('free')**"REPEAT")*Optional(Rule('statement_2'))),
Rule('statement_3'):  Rule('sentence')<<Optional(Rule('tag'))*Terminal(TUhE)*Optional(Rule('free')**"REPEAT")*Rule('text_1')*Elidable(Terminal(TUhU)*Optional(Rule('free')**"REPEAT")),
Rule('fragment'):  Rule('ek')*Optional(Rule('free')**"REPEAT")<<Rule('gihek')*Optional(Rule('free')**"REPEAT")<<Rule('quantifier')<<Terminal(NA)*Optional(Rule('free')**"REPEAT")<<Rule('terms')*Elidable(Terminal(VAU)*Optional(Rule('free')**"REPEAT"))<<Rule('prenex')<<Rule('relative_clauses')<<Rule('links')<<Rule('linkargs'),
Rule('prenex'):  Rule('terms')*Terminal(ZOhU)*Optional(Rule('free')**"REPEAT"),
Rule('sentence'):  Optional(Rule('terms')*Optional(Terminal(CU)*Optional(Rule('free')**"REPEAT")))*Rule('bridi_tail'),
Rule('subsentence'):  Rule('sentence')<<Rule('prenex')*Rule('subsentence'),
Rule('bridi_tail'):  Rule('bridi_tail_1')*Optional(Rule('gihek')*Optional(Rule('stag'))*Terminal(KE)*Optional(Rule('free')**"REPEAT")*Rule('bridi_tail')*Elidable(Terminal(KEhE)*Optional(Rule('free')**"REPEAT"))*Rule('tail_terms')),
Rule('bridi_tail_1'):  Rule('bridi_tail_2')*Optional(Rule('gihek')*Optional(Rule('free')**"REPEAT")*Rule('bridi_tail_2')*Rule('tail_terms'))**"REPEAT",
Rule('bridi_tail_2'):  Rule('bridi_tail_3')*Optional(Rule('gihek')*Optional(Rule('stag'))*Terminal(BO)*Optional(Rule('free')**"REPEAT")*Rule('bridi_tail_2')*Rule('tail_terms')),
Rule('bridi_tail_3'):  Rule('selbri')*Rule('tail_terms')<<Rule('gek_sentence'),
Rule('gek_sentence'):  Rule('gek')*Rule('subsentence')*Rule('gik')*Rule('subsentence')*Rule('tail_terms')<<Optional(Rule('tag'))*Terminal(KE)*Optional(Rule('free')**"REPEAT")*Rule('gek_sentence')*Elidable(Terminal(KEhE)*Optional(Rule('free')**"REPEAT"))<<Terminal(NA)*Optional(Rule('free')**"REPEAT")*Rule('gek_sentence'),
Rule('tail_terms'):  Optional(Rule('terms'))*Elidable(Terminal(VAU)*Optional(Rule('free')**"REPEAT")),
Rule('terms'):  Rule('terms_1')**"REPEAT",
Rule('terms_1'):  Rule('terms_2')*Optional(Terminal(PEhE)*Optional(Rule('free')**"REPEAT")*Rule('joik_jek')*Rule('terms_2'))**"REPEAT",
Rule('terms_2'):  Rule('term')*Optional(Terminal(CEhE)*Optional(Rule('free')**"REPEAT")*Rule('term'))**"REPEAT",
Rule('term'):  Rule('sumti')<<(Rule('tag')<<Terminal(FA)*Optional(Rule('free')**"REPEAT"))*(Rule('sumti')<<Elidable(Terminal(KU)*Optional(Rule('free')**"REPEAT")))<<Rule('termset')<<Terminal(NA)*Terminal(KU)*Optional(Rule('free')**"REPEAT"),
Rule('termset'):  Terminal(NUhI)*Optional(Rule('free')**"REPEAT")*Rule('gek')*Rule('terms')*Elidable(Terminal(NUhU)*Optional(Rule('free')**"REPEAT"))*Rule('gik')*Rule('terms')*Elidable(Terminal(NUhU)*Optional(Rule('free')**"REPEAT"))<<Terminal(NUhI)*Optional(Rule('free')**"REPEAT")*Rule('terms')*Elidable(Terminal(NUhU)*Optional(Rule('free')**"REPEAT")),
Rule('sumti'):  Rule('sumti_1')*Optional(Terminal(VUhO)*Optional(Rule('free')**"REPEAT")*Rule('relative_clauses')),
Rule('sumti_1'):  Rule('sumti_2')*Optional((Rule('ek')<<Rule('joik'))*Optional(Rule('stag'))*Terminal(KE)*Optional(Rule('free')**"REPEAT")*Rule('sumti')*Elidable(Terminal(KEhE)*Optional(Rule('free')**"REPEAT"))),
Rule('sumti_2'):  Rule('sumti_3')*Optional(Rule('joik_ek')*Rule('sumti_3'))**"REPEAT",
Rule('sumti_3'):  Rule('sumti_4')*Optional((Rule('ek')<<Rule('joik'))*Optional(Rule('stag'))*Terminal(BO)*Optional(Rule('free')**"REPEAT")*Rule('sumti_3')),
Rule('sumti_4'):  Rule('sumti_5')<<Rule('gek')*Rule('sumti')*Rule('gik')*Rule('sumti_4'),
Rule('sumti_5'):  Optional(Rule('quantifier'))*Rule('sumti_6')*Optional(Rule('relative_clauses'))<<Rule('quantifier')*Rule('selbri')*Elidable(Terminal(KU)*Optional(Rule('free')**"REPEAT"))*Optional(Rule('relative_clauses')),
Rule('sumti_6'):  (Terminal(LAhE)*Optional(Rule('free')**"REPEAT")<<Terminal(NAhE)*Terminal(BO)*Optional(Rule('free')**"REPEAT"))*Optional(Rule('relative_clauses'))*Rule('sumti')*Elidable(Terminal(LUhU)*Optional(Rule('free')**"REPEAT"))<<Terminal(KOhA)*Optional(Rule('free')**"REPEAT")<<Rule('lerfu_string')*Elidable(Terminal(BOI)*Optional(Rule('free')**"REPEAT"))<<Terminal(LA)*Optional(Rule('free')**"REPEAT")*Optional(Rule('relative_clauses'))*Terminal(CMENE)**"REPEAT"*Optional(Rule('free')**"REPEAT")<<(Terminal(LA)<<Terminal(LE))*Optional(Rule('free')**"REPEAT")*Rule('sumti_tail')*Elidable(Terminal(KU)*Optional(Rule('free')**"REPEAT"))<<Terminal(LI)*Optional(Rule('free')**"REPEAT")*Rule('mex')*Elidable(Terminal(LOhO)*Optional(Rule('free')**"REPEAT"))<<Terminal(ZO)*Rule('any_word')*Optional(Rule('free')**"REPEAT")<<Terminal(LU)*Rule('text')*Elidable(Terminal(LIhU)*Optional(Rule('free')**"REPEAT"))<<Terminal(LOhU)*Rule('any_word')**"REPEAT"*Terminal(LEhU)*Optional(Rule('free')**"REPEAT")<<Terminal(ZOI)*Rule('any_word')*Rule('anything')*Rule('any_word')*Optional(Rule('free')**"REPEAT"),
Rule('sumti_tail'):  Optional(Rule('sumti_6')*Optional(Rule('relative_clauses')))*Rule('sumti_tail_1')<<Rule('relative_clauses')*Rule('sumti_tail_1'),
Rule('sumti_tail_1'):  Optional(Rule('quantifier'))*Rule('selbri')*Optional(Rule('relative_clauses'))<<Rule('quantifier')*Rule('sumti'),
Rule('relative_clauses'):  Rule('relative_clause')*Optional(Terminal(ZIhE)*Optional(Rule('free')**"REPEAT")*Rule('relative_clause'))**"REPEAT",
Rule('relative_clause'):  Terminal(GOI)*Optional(Rule('free')**"REPEAT")*Rule('term')*Elidable(Terminal(GEhU)*Optional(Rule('free')**"REPEAT"))<<Terminal(NOI)*Optional(Rule('free')**"REPEAT")*Rule('subsentence')*Elidable(Terminal(KUhO)*Optional(Rule('free')**"REPEAT")),
Rule('selbri'):  Optional(Rule('tag'))*Rule('selbri_1'),
Rule('selbri_1'):  Rule('selbri_2')<<Terminal(NA)*Optional(Rule('free')**"REPEAT")*Rule('selbri'),
Rule('selbri_2'):  Rule('selbri_3')*Optional(Terminal(CO)*Optional(Rule('free')**"REPEAT")*Rule('selbri_2')),
Rule('selbri_3'):  Rule('selbri_4')**"REPEAT",
Rule('selbri_4'):  Rule('selbri_5')*Optional(Rule('joik_jek')*Rule('selbri_5')<<Rule('joik')*Optional(Rule('stag'))*Terminal(KE)*Optional(Rule('free')**"REPEAT")*Rule('selbri_3')*Elidable(Terminal(KEhE)*Optional(Rule('free')**"REPEAT")))**"REPEAT",
Rule('selbri_5'):  Rule('selbri_6')*Optional((Rule('jek')<<Rule('joik'))*Optional(Rule('stag'))*Terminal(BO)*Optional(Rule('free')**"REPEAT")*Rule('selbri_5')),
Rule('selbri_6'):  Rule('tanru_unit')*Optional(Terminal(BO)*Optional(Rule('free')**"REPEAT")*Rule('selbri_6'))<<Optional(Terminal(NAhE)*Optional(Rule('free')**"REPEAT"))*Rule('guhek')*Rule('selbri')*Rule('gik')*Rule('selbri_6'),
Rule('tanru_unit'):  Rule('tanru_unit_1')*Optional(Terminal(CEI)*Optional(Rule('free')**"REPEAT")*Rule('tanru_unit_1'))**"REPEAT",
Rule('tanru_unit_1'):  Rule('tanru_unit_2')*Optional(Rule('linkargs')),
Rule('tanru_unit_2'):  Terminal(BRIVLA)*Optional(Rule('free')**"REPEAT")<<Terminal(GOhA)*Optional(Terminal(RAhO))*Optional(Rule('free')**"REPEAT")<<Terminal(KE)*Optional(Rule('free')**"REPEAT")*Rule('selbri_3')*Elidable(Terminal(KEhE)*Optional(Rule('free')**"REPEAT"))<<Terminal(ME)*Optional(Rule('free')**"REPEAT")*Rule('sumti')*Elidable(Terminal(MEhU)*Optional(Rule('free')**"REPEAT"))*Optional(Terminal(MOI)*Optional(Rule('free')**"REPEAT"))<<(Rule('number')<<Rule('lerfu_string'))*Terminal(MOI)*Optional(Rule('free')**"REPEAT")<<Terminal(NUhA)*Optional(Rule('free')**"REPEAT")*Rule('mex_operator')<<Terminal(SE)*Optional(Rule('free')**"REPEAT")*Rule('tanru_unit_2')<<Terminal(JAI)*Optional(Rule('free')**"REPEAT")*Optional(Rule('tag'))*Rule('tanru_unit_2')<<Rule('any_word')*(Terminal(ZEI)*Rule('any_word'))**"REPEAT"<<Terminal(NAhE)*Optional(Rule('free')**"REPEAT")*Rule('tanru_unit_2')<<Terminal(NU)*Optional(Terminal(NAI))*Optional(Rule('free')**"REPEAT")*Optional(Rule('joik_jek')*Terminal(NU)*Optional(Terminal(NAI))*Optional(Rule('free')**"REPEAT"))**"REPEAT"*Rule('subsentence')*Elidable(Terminal(KEI)*Optional(Rule('free')**"REPEAT")),
Rule('linkargs'):  Terminal(BE)*Optional(Rule('free')**"REPEAT")*Rule('term')*Optional(Rule('links'))*Elidable(Terminal(BEhO)*Optional(Rule('free')**"REPEAT")),
Rule('links'):  Terminal(BEI)*Optional(Rule('free')**"REPEAT")*Rule('term')*Optional(Rule('links')),
Rule('quantifier'):  Rule('number')*Elidable(Terminal(BOI)*Optional(Rule('free')**"REPEAT"))<<Terminal(VEI)*Optional(Rule('free')**"REPEAT")*Rule('mex')*Elidable(Terminal(VEhO)*Optional(Rule('free')**"REPEAT")),
Rule('mex'):  Rule('mex_1')*Optional(Rule('operator')*Rule('mex_1'))**"REPEAT"<<Terminal(FUhA)*Optional(Rule('free')**"REPEAT")*Rule('rp_expression'),
Rule('mex_1'):  Rule('mex_2')*Optional(Terminal(BIhE)*Optional(Rule('free')**"REPEAT")*Rule('operator')*Rule('mex_1')),
Rule('mex_2'):  Rule('operand')<<Optional(Terminal(PEhO)*Optional(Rule('free')**"REPEAT"))*Rule('operator')*Rule('mex_2')**"REPEAT"*Elidable(Terminal(KUhE)*Optional(Rule('free')**"REPEAT")),
Rule('rp_expression'):  Rule('rp_operand')*Rule('rp_operand')*Rule('operator'),
Rule('rp_operand'):  Rule('operand')<<Rule('rp_expression'),
Rule('operator'):  Rule('operator_1')*Optional(Rule('joik_jek')*Rule('operator_1')<<Rule('joik')*Optional(Rule('stag'))*Terminal(KE)*Optional(Rule('free')**"REPEAT")*Rule('operator')*Elidable(Terminal(KEhE)*Optional(Rule('free')**"REPEAT")))**"REPEAT",
Rule('operator_1'):  Rule('operator_2')<<Rule('guhek')*Rule('operator_1')*Rule('gik')*Rule('operator_2')<<Rule('operator_2')*(Rule('jek')<<Rule('joik'))*Optional(Rule('stag'))*Terminal(BO)*Optional(Rule('free')**"REPEAT")*Rule('operator_1'),
Rule('operator_2'):  Rule('mex_operator')<<Terminal(KE)*Optional(Rule('free')**"REPEAT")*Rule('operator')*Elidable(Terminal(KEhE)*Optional(Rule('free')**"REPEAT")),
Rule('mex_operator'):  Terminal(SE)*Optional(Rule('free')**"REPEAT")*Rule('mex_operator')<<Terminal(NAhE)*Optional(Rule('free')**"REPEAT")*Rule('mex_operator')<<Terminal(MAhO)*Optional(Rule('free')**"REPEAT")*Rule('mex')*Elidable(Terminal(TEhU)*Optional(Rule('free')**"REPEAT"))<<Terminal(NAhU)*Optional(Rule('free')**"REPEAT")*Rule('selbri')*Elidable(Terminal(TEhU)*Optional(Rule('free')**"REPEAT"))<<Terminal(VUhU)*Optional(Rule('free')**"REPEAT"),
Rule('operand'):  Rule('operand_1')*Optional((Rule('ek')<<Rule('joik'))*Optional(Rule('stag'))*Terminal(KE)*Optional(Rule('free')**"REPEAT")*Rule('operand')*Elidable(Terminal(KEhE)*Optional(Rule('free')**"REPEAT"))),
Rule('operand_1'):  Rule('operand_2')*Optional(Rule('joik_ek')*Rule('operand_2'))**"REPEAT",
Rule('operand_2'):  Rule('operand_3')*Optional((Rule('ek')<<Rule('joik'))*Optional(Rule('stag'))*Terminal(BO)*Optional(Rule('free')**"REPEAT")*Rule('operand_2')),
Rule('operand_3'):  Rule('quantifier')<<Rule('lerfu_string')*Elidable(Terminal(BOI)*Optional(Rule('free')**"REPEAT"))<<Terminal(NIhE)*Optional(Rule('free')**"REPEAT")*Rule('selbri')*Elidable(Terminal(TEhU)*Optional(Rule('free')**"REPEAT"))<<Terminal(MOhE)*Optional(Rule('free')**"REPEAT")*Rule('sumti')*Elidable(Terminal(TEhU)*Optional(Rule('free')**"REPEAT"))<<Terminal(JOhI)*Optional(Rule('free')**"REPEAT")*Rule('mex_2')**"REPEAT"*Elidable(Terminal(TEhU)*Optional(Rule('free')**"REPEAT"))<<Rule('gek')*Rule('operand')*Rule('gik')*Rule('operand_3')<<(Terminal(LAhE)*Optional(Rule('free')**"REPEAT")<<Terminal(NAhE)*Terminal(BO)*Optional(Rule('free')**"REPEAT"))*Rule('operand')*Elidable(Terminal(LUhU)*Optional(Rule('free')**"REPEAT")),
Rule('number'):  Terminal(PA)*Optional(Terminal(PA)<<Rule('lerfu_word'))**"REPEAT",
Rule('lerfu_string'):  Rule('lerfu_word')*Optional(Terminal(PA)<<Rule('lerfu_word'))**"REPEAT",
Rule('lerfu_word'):  Terminal(BY)<<Rule('any_word')*Terminal(BU)<<Terminal(LAU)*Rule('lerfu_word')<<Terminal(TEI)*Rule('lerfu_string')*Terminal(FOI),
Rule('ek'):  Optional(Terminal(NA))*Optional(Terminal(SE))*Terminal(A)*Optional(Terminal(NAI)),
Rule('gihek'):  Optional(Terminal(NA))*Optional(Terminal(SE))*Terminal(GIhA)*Optional(Terminal(NAI)),
Rule('jek'):  Optional(Terminal(NA))*Optional(Terminal(SE))*Terminal(JA)*Optional(Terminal(NAI)),
Rule('joik'):  Optional(Terminal(SE))*Terminal(JOI)*Optional(Terminal(NAI))<<Rule('interval')<<Terminal(GAhO)*Rule('interval')*Terminal(GAhO),
Rule('interval'):  Optional(Terminal(SE))*Terminal(BIhI)*Optional(Terminal(NAI)),
Rule('joik_ek'):  Rule('joik')*Optional(Rule('free')**"REPEAT")<<Rule('ek')*Optional(Rule('free')**"REPEAT"),
Rule('joik_jek'):  Rule('joik')*Optional(Rule('free')**"REPEAT")<<Rule('jek')*Optional(Rule('free')**"REPEAT"),
Rule('gek'):  Optional(Terminal(SE))*Terminal(GA)*Optional(Terminal(NAI))*Optional(Rule('free')**"REPEAT")<<Rule('joik')*Terminal(GI)*Optional(Rule('free')**"REPEAT")<<Rule('stag')*Rule('gik'),
Rule('guhek'):  Optional(Terminal(SE))*Terminal(GUhA)*Optional(Terminal(NAI))*Optional(Rule('free')**"REPEAT"),
Rule('gik'):  Terminal(GI)*Optional(Terminal(NAI))*Optional(Rule('free')**"REPEAT"),
Rule('tag'):  Rule('tense_modal')*Optional(Rule('joik_jek')*Rule('tense_modal'))**"REPEAT",
Rule('stag'):  Rule('simple_tense_modal')*Optional((Rule('jek')<<Rule('joik'))*Rule('simple_tense_modal'))**"REPEAT",
Rule('tense_modal'):  Rule('simple_tense_modal')*Optional(Rule('free')**"REPEAT")<<Terminal(FIhO)*Optional(Rule('free')**"REPEAT")*Rule('selbri')*Elidable(Terminal(FEhU)*Optional(Rule('free')**"REPEAT")),
Rule('simple_tense_modal'):  Optional(Terminal(NAhE))*Optional(Terminal(SE))*Terminal(BAI)*Optional(Terminal(NAI))*Optional(Terminal(KI))<<Optional(Terminal(NAhE))*(Rule('time')*Optional(Rule('space'))<<Rule('space')*Optional(Rule('time')))+Terminal(CAhA)*Optional(Terminal(KI))<<Terminal(KI)<<Terminal(CUhE),
Rule('time'):  Terminal(ZI)+Rule('time_offset')**"REPEAT"+Terminal(ZEhA)*Optional(Terminal(PU)*Optional(Terminal(NAI)))+Rule('interval_property')**"REPEAT",
Rule('time_offset'):  Terminal(PU)*Optional(Terminal(NAI))*Optional(Terminal(ZI)),
Rule('space'):  Terminal(VA)+Rule('space_offset')**"REPEAT"+Rule('space_interval')+(Terminal(MOhI)*Rule('space_offset')),
Rule('space_offset'):  Terminal(FAhA)*Optional(Terminal(NAI))*Optional(Terminal(VA)),
Rule('space_interval'):  ((Terminal(VEhA)+Terminal(VIhA))*Optional(Terminal(FAhA)*Optional(Terminal(NAI))))+Rule('space_int_props'),
Rule('space_int_props'):  (Terminal(FEhE)*Rule('interval_property'))**"REPEAT",
Rule('interval_property'):  Rule('number')*Terminal(ROI)*Optional(Terminal(NAI))<<Terminal(TAhE)*Optional(Terminal(NAI))<<Terminal(ZAhO)*Optional(Terminal(NAI)),
Rule('free'):  Terminal(SEI)*Optional(Rule('free')**"REPEAT")*Optional(Rule('terms')*Optional(Terminal(CU)*Optional(Rule('free')**"REPEAT")))*Rule('selbri')*Elidable(Terminal(SEhU))<<Terminal(SOI)*Optional(Rule('free')**"REPEAT")*Rule('sumti')*Optional(Rule('sumti'))*Elidable(Terminal(SEhU))<<Rule('vocative')*Optional(Rule('relative_clauses'))*Rule('selbri')*Optional(Rule('relative_clauses'))*Elidable(Terminal(DOhU))<<Rule('vocative')*Optional(Rule('relative_clauses'))*Terminal(CMENE)**"REPEAT"*Optional(Rule('free')**"REPEAT")*Optional(Rule('relative_clauses'))*Elidable(Terminal(DOhU))<<Rule('vocative')*Optional(Rule('sumti'))*Elidable(Terminal(DOhU))<<(Rule('number')<<Rule('lerfu_string'))*Terminal(MAI)<<Terminal(TO)*Rule('text')*Elidable(Terminal(TOI))<<Terminal(XI)*Optional(Rule('free')**"REPEAT")*(Rule('number')<<Rule('lerfu_string'))*Elidable(Terminal(BOI))<<Terminal(XI)*Optional(Rule('free')**"REPEAT")*Terminal(VEI)*Optional(Rule('free')**"REPEAT")*Rule('mex')*Elidable(Terminal(VEhO)),
Rule('vocative'):  (Terminal(COI)*Optional(Terminal(NAI)))**"REPEAT"+Terminal(DOI),
Rule('indicators'):  Optional(Terminal(FUhE))*Rule('indicator')**"REPEAT",
Rule('indicator'):  (Terminal(UI)<<Terminal(CAI))*Optional(Terminal(NAI))<<Terminal(Y)<<Terminal(DAhO)<<Terminal(FUhO),
Rule('lerfu_word'):  Terminal(BY)<<Terminal(BU)<<Terminal(LAU)*Rule('lerfu_word')<<Terminal(TEI)*Rule('lerfu_string')*Terminal(FOI),
Rule('tanru_unit_2'):  Terminal(BRIVLA)*Optional(Rule('free')**"REPEAT")<<Terminal(GOhA)*Optional(Terminal(RAhO))*Optional(Rule('free')**"REPEAT")<<Terminal(KE)*Optional(Rule('free')**"REPEAT")*Rule('selbri_3')*Elidable(Terminal(KEhE)*Optional(Rule('free')**"REPEAT"))<<Terminal(ME)*Optional(Rule('free')**"REPEAT")*Rule('sumti')*Elidable(Terminal(MEhU)*Optional(Rule('free')**"REPEAT"))*Optional(Terminal(MOI)*Optional(Rule('free')**"REPEAT"))<<(Rule('number')<<Rule('lerfu_string'))*Terminal(MOI)*Optional(Rule('free')**"REPEAT")<<Terminal(NUhA)*Optional(Rule('free')**"REPEAT")*Rule('mex_operator')<<Terminal(SE)*Optional(Rule('free')**"REPEAT")*Rule('tanru_unit_2')<<Terminal(JAI)*Optional(Rule('free')**"REPEAT")*Optional(Rule('tag'))*Rule('tanru_unit_2')<<Terminal(NAhE)*Optional(Rule('free')**"REPEAT")*Rule('tanru_unit_2')<<Terminal(NU)*Optional(Terminal(NAI))*Optional(Rule('free')**"REPEAT")*Optional(Rule('joik_jek')*Terminal(NU)*Optional(Terminal(NAI))*Optional(Rule('free')**"REPEAT"))**"REPEAT"*Rule('subsentence')*Elidable(Terminal(KEI)*Optional(Rule('free')**"REPEAT")),
Rule('lerfu_word'):  Terminal(BY)<<Terminal(BU)<<Terminal(LAU)*Rule('lerfu_word')<<Terminal(TEI)*Rule('lerfu_string')*Terminal(FOI),
Rule('sumti_6'):  (Terminal(LAhE)*Optional(Rule('free')**"REPEAT")<<Terminal(NAhE)*Terminal(BO)*Optional(Rule('free')**"REPEAT"))*Optional(Rule('relative_clauses'))*Rule('sumti')*Elidable(Terminal(LUhU)*Optional(Rule('free')**"REPEAT"))<<Terminal(KOhA)*Optional(Rule('free')**"REPEAT")<<Rule('lerfu_string')*Elidable(Terminal(BOI)*Optional(Rule('free')**"REPEAT"))<<Terminal(LA)*Optional(Rule('free')**"REPEAT")*Optional(Rule('relative_clauses'))*Terminal(CMENE)**"REPEAT"*Optional(Rule('free')**"REPEAT")<<(Terminal(LA)<<Terminal(LE))*Optional(Rule('free')**"REPEAT")*Rule('sumti_tail')*Elidable(Terminal(KU)*Optional(Rule('free')**"REPEAT"))<<Terminal(LI)*Optional(Rule('free')**"REPEAT")*Rule('mex')*Elidable(Terminal(LOhO)*Optional(Rule('free')**"REPEAT"))<<Terminal(ZO)*Optional(Rule('free')**"REPEAT")<<Terminal(LU)*Rule('text')*Elidable(Terminal(LIhU)*Optional(Rule('free')**"REPEAT"))<<Terminal(LOhU)*Terminal(LEhU)*Optional(Rule('free')**"REPEAT")<<Terminal(ZOI)*Optional(Rule('free')**"REPEAT"),
Rule('x_parse_root'):  Rule('text'),
Rule('x_test'):  Rule('x_test_issue_3'),
Rule('x_test_issue_1'):  Terminal(LA)*Terminal(CMENE)**"REPEAT"<<Terminal(LA)*Terminal(SELBRI),
Rule('x_test_issue_2'):  Rule('a')*Optional(Rule('b'))**"REPEAT",
Rule('x_test_issue_3'):  Rule('x_test_issue_3_bit_1')*Terminal(KOhA),
Rule('x_test_issue_3_bit_1'):  Terminal(LAhE)*Rule('x_test_issue_3_bit_2')*Elidable(Terminal(LUhU)*Optional(Rule('free')**"REPEAT")),
Rule('x_test_issue_3_bit_2'):  Terminal(KOhA)<<Rule('x_test_issue_3_bit_1'),
Rule('a'):  Terminal(A),
Rule('b'):  Terminal(CMENE),
Rule('x_test_cat'):  Rule('a')*Rule('b'),
Rule('x_test_cat_2'):  Rule('a')*Rule('b')**"REPEAT",
Rule('x_test_xor'):  Rule('a')<<Rule('b'),
Rule('x_test_and'):  Rule('a')+Rule('b'),
Rule('x_test_optional_1'):  Rule('a')*Optional(Rule('b')),
Rule('x_test_optional_2'):  Optional(Rule('b'))*Rule('a'),
Rule('x_test_optional_3'):  Rule('a')*Optional(Rule('x_test_optional_3_bit'))*Rule('a'),
Rule('x_test_optional_3_bit'):  Optional(Rule('b')),
Rule('x_test_elide'):  Rule('x_test_elide_bit_1')*Optional(Rule('x_test_elide_bit_2')),
Rule('x_test_elide_bit_1'):  (Terminal(LE)*Terminal(SELBRI)**"REPEAT")<<Terminal(KOhA),
Rule('x_test_elide_bit_2'):  (Elidable(Terminal(CU))*Terminal(SELBRI))<<Terminal(PA),
Rule('x_inefficiency_example'):  Rule('a')*Rule('b')*Rule('c')
}

BNF['any_word'] = any_word()
BNF['unmatched'] = 'unmatched' 
if __name__ == '__main__':
  if len(sys.argv) > 1:
    for key in sys.argv[1:]:
      print (key, ":", BNF[key])
  else:
    print (BNF)

