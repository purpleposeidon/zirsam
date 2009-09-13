# -*- coding: utf-8 -*-

# generated on Sat Sep 12 18:09:24 2009 by poseidon@skami

from bnfgen import *

rules = {
  Rule('sumti-tail111') :
     (Optional(Rule('sumti-6'), Optional(Rule('relative-clauses'))), Or(Rule('sumti-tail-1'), Rule('relative-clauses')), Rule('sumti-tail-1')) ,\
  Rule('operand381') :
     (Rule('operand-1'), Optional(Paren(Or(Rule('ek'), Rule('joik'))), Optional(Rule('stag')), Terminal(KE), Optional(Repeated(Rule('free'))), Rule('operand'), Elidable(Terminal(KEhE), Optional(Repeated(Rule('free')))))) ,\
  Rule('gek807') :
     (Optional(Terminal(SE)), Terminal(GA), Optional(Terminal(NAI)), Or(Optional(Repeated(Rule('free'))), Rule('joik')), Terminal(GI), Or(Optional(Repeated(Rule('free'))), Rule('stag')), Rule('gik')) ,\
  Rule('sumti-tail-1112') :
     (Optional(Rule('quantifier')), Rule('selbri'), Or(Optional(Rule('relative-clauses')), Rule('quantifier')), Rule('sumti')) ,\
  Rule('mex310') :
     (Rule('mex-1'), Or(Repeated(Optional(Rule('operator'), Rule('mex-1'))), Terminal(FUhA)), Optional(Repeated(Rule('free'))), Rule('rp-expression')) ,\
  Rule('selbri130') :
     (Optional(Rule('tag')), Rule('selbri-1')) ,\
  Rule('term83') :
     (Or(Rule('sumti'), Paren(Or(Rule('tag'), Terminal(FA)), Optional(Repeated(Rule('free'))))), Or(Or(Paren(Or(Rule('sumti'), Elidable(Terminal(KU), Optional(Repeated(Rule('free')))))), Rule('termset')), Terminal(NA)), Terminal(KU), Optional(Repeated(Rule('free')))) ,\
  Rule('linkargs160') :
     (Terminal(BE), Optional(Repeated(Rule('free'))), Rule('term'), Optional(Rule('links')), Elidable(Terminal(BEhO), Optional(Repeated(Rule('free'))))) ,\
  Rule('selbri-1131') :
     (Or(Rule('selbri-2'), Terminal(NA)), Optional(Repeated(Rule('free'))), Rule('selbri')) ,\
  Rule('free32') :
     (Terminal(SEI), Optional(Repeated(Rule('free'))), Optional(Rule('terms'), Optional(Terminal(CU), Optional(Repeated(Rule('free'))))), Rule('selbri'), Or(Elidable(Terminal(SEhU)), Terminal(SOI)), Optional(Repeated(Rule('free'))), Rule('sumti'), Optional(Rule('sumti')), Or(Elidable(Terminal(SEhU)), Rule('vocative')), Optional(Rule('relative-clauses')), Rule('selbri'), Optional(Rule('relative-clauses')), Or(Elidable(Terminal(DOhU)), Rule('vocative')), Optional(Rule('relative-clauses')), Repeated(Terminal(<class 'tokens.CMENE'>)), Optional(Repeated(Rule('free'))), Optional(Rule('relative-clauses')), Or(Elidable(Terminal(DOhU)), Rule('vocative')), Optional(Rule('sumti')), Or(Elidable(Terminal(DOhU)), Paren(Or(Rule('number'), Rule('lerfu-string')))), Or(Terminal(MAI), Terminal(TO)), Rule('text'), Or(Elidable(Terminal(TOI)), Terminal(XI)), Optional(Repeated(Rule('free'))), Paren(Or(Rule('number'), Rule('lerfu-string'))), Or(Elidable(Terminal(BOI)), Terminal(XI)), Optional(Repeated(Rule('free'))), Terminal(VEI), Optional(Repeated(Rule('free'))), Rule('mex'), Elidable(Terminal(VEhO))) ,\
  Rule('relative-clause122') :
     (Terminal(GOI), Optional(Repeated(Rule('free'))), Rule('term'), Or(Elidable(Terminal(GEhU), Optional(Repeated(Rule('free')))), Terminal(NOI)), Optional(Repeated(Rule('free'))), Rule('subsentence'), Elidable(Terminal(KUhO), Optional(Repeated(Rule('free'))))) ,\
  Rule('tense-modal815') :
     (Rule('simple-tense-modal'), Or(Optional(Repeated(Rule('free'))), Terminal(FIhO)), Optional(Repeated(Rule('free'))), Rule('selbri'), Elidable(Terminal(FEhU), Optional(Repeated(Rule('free'))))) ,\
  Rule('number812') :
     (Terminal(PA), Repeated(Optional(Or(Terminal(PA), Rule('lerfu-word'))))) ,\
  Rule('operand-3385') :
     (Or(Rule('quantifier'), Rule('lerfu-string')), Or(Elidable(Terminal(BOI), Optional(Repeated(Rule('free')))), Terminal(NIhE)), Optional(Repeated(Rule('free'))), Rule('selbri'), Or(Elidable(Terminal(TEhU), Optional(Repeated(Rule('free')))), Terminal(MOhE)), Optional(Repeated(Rule('free'))), Rule('sumti'), Or(Elidable(Terminal(TEhU), Optional(Repeated(Rule('free')))), Terminal(JOhI)), Optional(Repeated(Rule('free'))), Repeated(Rule('mex-2')), Or(Elidable(Terminal(TEhU), Optional(Repeated(Rule('free')))), Rule('gek')), Rule('operand'), Rule('gik'), Or(Rule('operand-3'), Paren(Terminal(LAhE), Or(Optional(Repeated(Rule('free'))), Terminal(NAhE)), Terminal(BO), Optional(Repeated(Rule('free'))))), Rule('operand'), Elidable(Terminal(LUhU), Optional(Repeated(Rule('free'))))) ,\
  Rule('jek805') :
     (Optional(Terminal(NA)), Optional(Terminal(SE)), Terminal(JA), Optional(Terminal(NAI))) ,\
  Rule('paragraph10') :
     (Paren(Or(Rule('statement'), Rule('fragment'))), Repeated(Optional(Terminal(I), Optional(Repeated(Rule('free'))), Optional(Or(Rule('statement'), Rule('fragment')))))) ,\
  Rule('mex-1311') :
     (Rule('mex-2'), Optional(Terminal(BIhE), Optional(Repeated(Rule('free'))), Rule('operator'), Rule('mex-1'))) ,\
  Rule('indicators411') :
     (Optional(Terminal(FUhE)), Repeated(Rule('indicator'))) ,\
  Rule('bridi-tail50') :
     (Rule('bridi-tail-1'), Optional(Rule('gihek'), Optional(Rule('stag')), Terminal(KE), Optional(Repeated(Rule('free'))), Rule('bridi-tail'), Elidable(Terminal(KEhE), Optional(Repeated(Rule('free')))), Rule('tail-terms'))) ,\
  Rule('guhek808') :
     (Optional(Terminal(SE)), Terminal(GUhA), Optional(Terminal(NAI)), Optional(Repeated(Rule('free')))) ,\
  Rule('statement-314') :
     (Or(Rule('sentence'), Optional(Rule('tag'))), Terminal(TUhE), Optional(Repeated(Rule('free'))), Rule('text-1'), Elidable(Terminal(TUhU), Optional(Repeated(Rule('free'))))) ,\
  Rule('gihek818') :
     (Optional(Terminal(NA)), Optional(Terminal(SE)), Terminal(GIhA), Optional(Terminal(NAI))) ,\
  Rule('gek-sentence54') :
     (Rule('gek'), Rule('subsentence'), Rule('gik'), Rule('subsentence'), Or(Rule('tail-terms'), Optional(Rule('tag'))), Terminal(KE), Optional(Repeated(Rule('free'))), Rule('gek-sentence'), Or(Elidable(Terminal(KEhE), Optional(Repeated(Rule('free')))), Terminal(NA)), Optional(Repeated(Rule('free'))), Rule('gek-sentence')) ,\
  Rule('joik-ek421') :
     (Rule('joik'), Or(Optional(Repeated(Rule('free'))), Rule('ek')), Optional(Repeated(Rule('free')))) ,\
  Rule('stag971') :
     (Rule('simple-tense-modal'), Repeated(Optional(Paren(Or(Rule('jek'), Rule('joik'))), Rule('simple-tense-modal')))) ,\
  Rule('sumti-393') :
     (Rule('sumti-4'), Optional(Paren(Or(Rule('ek'), Rule('joik'))), Optional(Rule('stag')), Terminal(BO), Optional(Repeated(Rule('free'))), Rule('sumti-3'))) ,\
  Rule('links161') :
     (Terminal(BEI), Optional(Repeated(Rule('free'))), Rule('term'), Optional(Rule('links'))) ,\
  Rule('bridi-tail-151') :
     (Rule('bridi-tail-2'), Repeated(Optional(Rule('gihek'), Optional(Repeated(Rule('free'))), Rule('bridi-tail-2'), Rule('tail-terms')))) ,\
  Rule('bridi-tail-252') :
     (Rule('bridi-tail-3'), Optional(Rule('gihek'), Optional(Rule('stag')), Terminal(BO), Optional(Repeated(Rule('free'))), Rule('bridi-tail-2'), Rule('tail-terms'))) ,\
  Rule('space-interval1046') :
     AndOr(Paren(Paren(AndOr(Terminal(VEhA), Terminal(VIhA))), Optional(Terminal(FAhA), Optional(Terminal(NAI)))), Rule('space-int-props')) ,\
  Rule('ek802') :
     (Optional(Terminal(NA)), Optional(Terminal(SE)), Terminal(A), Optional(Terminal(NAI))) ,\
  Rule('tail-terms71') :
     (Optional(Rule('terms')), Elidable(Terminal(VAU), Optional(Repeated(Rule('free'))))) ,\
  Rule('indicator413') :
     (Paren(Or(Terminal(UI), Terminal(CAI))), Or(Or(Or(Optional(Terminal(NAI)), Terminal(Y)), Terminal(DAhO)), Terminal(FUhO))) ,\
  Rule('selbri-6136') :
     (Rule('tanru-unit'), Or(Optional(Terminal(BO), Optional(Repeated(Rule('free'))), Rule('selbri-6')), Optional(Terminal(NAhE), Optional(Repeated(Rule('free'))))), Rule('guhek'), Rule('selbri'), Rule('gik'), Rule('selbri-6')) ,\
  Rule('terms80') :
     Repeated(Rule('terms-1')) ,\
  Rule('sumti-595') :
     (Optional(Rule('quantifier')), Rule('sumti-6'), Or(Optional(Rule('relative-clauses')), Rule('quantifier')), Rule('selbri'), Elidable(Terminal(KU), Optional(Repeated(Rule('free')))), Optional(Rule('relative-clauses'))) ,\
  Rule('interval-property1051') :
     (Rule('number'), Terminal(ROI), Or(Optional(Terminal(NAI)), Terminal(TAhE)), Or(Optional(Terminal(NAI)), Terminal(ZAhO)), Optional(Terminal(NAI))) ,\
  Rule('prenex30') :
     (Rule('terms'), Terminal(ZOhU), Optional(Repeated(Rule('free')))) ,\
  Rule('quantifier300') :
     (Rule('number'), Or(Elidable(Terminal(BOI), Optional(Repeated(Rule('free')))), Terminal(VEI)), Optional(Repeated(Rule('free'))), Rule('mex'), Elidable(Terminal(VEhO), Optional(Repeated(Rule('free'))))) ,\
  Rule('gik816') :
     (Terminal(GI), Optional(Terminal(NAI)), Optional(Repeated(Rule('free')))) ,\
  Rule('terms-282') :
     (Rule('term'), Repeated(Optional(Terminal(CEhE), Optional(Repeated(Rule('free'))), Rule('term')))) ,\
  Rule('joik-jek422') :
     (Rule('joik'), Or(Optional(Repeated(Rule('free'))), Rule('jek')), Optional(Repeated(Rule('free')))) ,\
  Rule('paragraphs4') :
     (Rule('paragraph'), Optional(Repeated(Terminal(NIhO)), Optional(Repeated(Rule('free'))), Rule('paragraphs'))) ,\
  Rule('rp-expression330') :
     (Rule('rp-operand'), Rule('rp-operand'), Rule('operator')) ,\
  Rule('subsentence41') :
     (Or(Rule('sentence'), Rule('prenex')), Rule('subsentence')) ,\
  Rule('joik806') :
     (Optional(Terminal(SE)), Terminal(JOI), Or(Or(Optional(Terminal(NAI)), Rule('interval')), Terminal(GAhO)), Rule('interval'), Terminal(GAhO)) ,\
  Rule('interval932') :
     (Optional(Terminal(SE)), Terminal(BIhI), Optional(Terminal(NAI))) ,\
  Rule('text-12') :
     (Optional(Or(Repeated(Paren(Terminal(I), Optional(Or(Rule('jek'), Rule('joik'))), Optional(Optional(Rule('stag')), Terminal(BO)), Optional(Repeated(Rule('free'))))), Repeated(Terminal(NIhO))), Optional(Repeated(Rule('free')))), Optional(Rule('paragraphs'))) ,\
  Rule('time1030') :
     (AndOr(AndOr(Terminal(ZI), Repeated(Rule('time-offset'))), Terminal(ZEhA)), AndOr(Optional(Terminal(PU), Optional(Terminal(NAI))), Repeated(Rule('interval-property')))) ,\
  Rule('rp-operand332') :
     Or(Rule('operand'), Rule('rp-expression')) ,\
  Rule('operator370') :
     (Rule('operator-1'), Repeated(Optional(Rule('joik-jek'), Or(Rule('operator-1'), Rule('joik')), Optional(Rule('stag')), Terminal(KE), Optional(Repeated(Rule('free'))), Rule('operator'), Elidable(Terminal(KEhE), Optional(Repeated(Rule('free'))))))) ,\
  Rule('simple-tense-modal972') :
     (Optional(Terminal(NAhE)), Optional(Terminal(SE)), Terminal(BAI), Optional(Terminal(NAI)), Or(Optional(Terminal(KI)), Optional(Terminal(NAhE))), AndOr(Paren(Rule('time'), Or(Optional(Rule('space')), Rule('space')), Optional(Rule('time'))), Terminal(CAhA)), Or(Or(Optional(Terminal(KI)), Terminal(KI)), Terminal(CUhE))) ,\
  Rule('mex-operator374') :
     (Terminal(SE), Optional(Repeated(Rule('free'))), Or(Rule('mex-operator'), Terminal(NAhE)), Optional(Repeated(Rule('free'))), Or(Rule('mex-operator'), Terminal(MAhO)), Optional(Repeated(Rule('free'))), Rule('mex'), Or(Elidable(Terminal(TEhU), Optional(Repeated(Rule('free')))), Terminal(NAhU)), Optional(Repeated(Rule('free'))), Rule('selbri'), Or(Elidable(Terminal(TEhU), Optional(Repeated(Rule('free')))), Terminal(VUhU)), Optional(Repeated(Rule('free')))) ,\
  Rule('tanru-unit150') :
     (Rule('tanru-unit-1'), Repeated(Optional(Terminal(CEI), Optional(Repeated(Rule('free'))), Rule('tanru-unit-1')))) ,\
  Rule('text0') :
     (Optional(Repeated(Terminal(NAI))), Optional(Repeated(Terminal(<class 'tokens.CMENE'>)), Or(Optional(Repeated(Rule('free'))), Paren(AndOr(Rule('indicators'), Repeated(Rule('free')))))), Optional(Rule('joik-jek')), Rule('text-1')) ,\
  Rule('selbri-5135') :
     (Rule('selbri-6'), Optional(Paren(Or(Rule('jek'), Rule('joik'))), Optional(Rule('stag')), Terminal(BO), Optional(Repeated(Rule('free'))), Rule('selbri-5'))) ,\
  Rule('space-offset1045') :
     (Terminal(FAhA), Optional(Terminal(NAI)), Optional(Terminal(VA))) ,\
  Rule('tanru-unit-1151') :
     (Rule('tanru-unit-2'), Optional(Rule('linkargs'))) ,\
  Rule('space-int-props1049') :
     Repeated(Paren(Terminal(FEhE), Rule('interval-property'))) ,\
  Rule('selbri-4134') :
     (Rule('selbri-5'), Repeated(Optional(Rule('joik-jek'), Or(Rule('selbri-5'), Rule('joik')), Optional(Rule('stag')), Terminal(KE), Optional(Repeated(Rule('free'))), Rule('selbri-3'), Elidable(Terminal(KEhE), Optional(Repeated(Rule('free'))))))) ,\
  Rule('relative-clauses121') :
     (Rule('relative-clause'), Repeated(Optional(Terminal(ZIhE), Optional(Repeated(Rule('free'))), Rule('relative-clause')))) ,\
  Rule('tag491') :
     (Rule('tense-modal'), Repeated(Optional(Rule('joik-jek'), Rule('tense-modal')))) ,\
  Rule('operand-2383') :
     (Rule('operand-3'), Optional(Paren(Or(Rule('ek'), Rule('joik'))), Optional(Rule('stag')), Terminal(BO), Optional(Repeated(Rule('free'))), Rule('operand-2'))) ,\
  Rule('fragment20') :
     (Rule('ek'), Or(Optional(Repeated(Rule('free'))), Rule('gihek')), Or(Or(Optional(Repeated(Rule('free'))), Rule('quantifier')), Terminal(NA)), Or(Optional(Repeated(Rule('free'))), Rule('terms')), Or(Or(Or(Or(Elidable(Terminal(VAU), Optional(Repeated(Rule('free')))), Rule('prenex')), Rule('relative-clauses')), Rule('links')), Rule('linkargs'))) ,\
  Rule('bridi-tail-353') :
     (Rule('selbri'), Or(Rule('tail-terms'), Rule('gek-sentence'))) ,\
  Rule('space1040') :
     AndOr(AndOr(AndOr(Terminal(VA), Repeated(Rule('space-offset'))), Rule('space-interval')), Paren(Terminal(MOhI), Rule('space-offset'))) ,\
  Rule('termset85') :
     (Terminal(NUhI), Optional(Repeated(Rule('free'))), Rule('gek'), Rule('terms'), Elidable(Terminal(NUhU), Optional(Repeated(Rule('free')))), Rule('gik'), Rule('terms'), Or(Elidable(Terminal(NUhU), Optional(Repeated(Rule('free')))), Terminal(NUhI)), Optional(Repeated(Rule('free'))), Rule('terms'), Elidable(Terminal(NUhU), Optional(Repeated(Rule('free'))))) ,\
  Rule('mex-2312') :
     (Or(Rule('operand'), Optional(Terminal(PEhO), Optional(Repeated(Rule('free'))))), Rule('operator'), Repeated(Rule('mex-2')), Elidable(Terminal(KUhE), Optional(Repeated(Rule('free'))))) ,\
  Rule('selbri-3133') :
     Repeated(Rule('selbri-4')) ,\
  Rule('sttement11') :
     (Or(Rule('statement-1'), Rule('prenex')), Rule('statement')) ,\
  Rule('sumti-191') :
     (Rule('sumti-2'), Optional(Paren(Or(Rule('ek'), Rule('joik'))), Optional(Rule('stag')), Terminal(KE), Optional(Repeated(Rule('free'))), Rule('sumti'), Elidable(Terminal(KEhE), Optional(Repeated(Rule('free')))))) ,\
  Rule('vocative415') :
     AndOr(Repeated(Paren(Terminal(COI), Optional(Terminal(NAI)))), Terminal(DOI)) ,\
  Rule('statement-213') :
     (Rule('statement-3'), Optional(Terminal(I), Optional(Or(Rule('jek'), Rule('joik'))), Optional(Rule('stag')), Terminal(BO), Optional(Repeated(Rule('free'))), Optional(Rule('statement-2')))) ,\
  Rule('operator-1371') :
     (Or(Rule('operator-2'), Rule('guhek')), Rule('operator-1'), Rule('gik'), Or(Rule('operator-2'), Rule('operator-2')), Paren(Or(Rule('jek'), Rule('joik'))), Optional(Rule('stag')), Terminal(BO), Optional(Repeated(Rule('free'))), Rule('operator-1')) ,\
  Rule('terms-181') :
     (Rule('terms-2'), Repeated(Optional(Terminal(PEhE), Optional(Repeated(Rule('free'))), Rule('joik-jek'), Rule('terms-2')))) ,\
  Rule('sumti-292') :
     (Rule('sumti-3'), Repeated(Optional(Rule('joik-ek'), Rule('sumti-3')))) ,\
  Rule('operand-1382') :
     (Rule('operand-2'), Repeated(Optional(Rule('joik-ek'), Rule('operand-2')))) ,\
  Rule('lerfu-string817') :
     (Rule('lerfu-word'), Repeated(Optional(Or(Terminal(PA), Rule('lerfu-word'))))) ,\
  Rule('sumti90') :
     (Rule('sumti-1'), Optional(Terminal(VUhO), Optional(Repeated(Rule('free'))), Rule('relative-clauses'))) ,\
  Rule('statement-112') :
     (Rule('statement-2'), Repeated(Optional(Terminal(I), Rule('joik-jek'), Optional(Rule('statement-2'))))) ,\
  Rule('sumti-697') :
     (Paren(Terminal(LAhE), Or(Optional(Repeated(Rule('free'))), Terminal(NAhE)), Terminal(BO), Optional(Repeated(Rule('free')))), Optional(Rule('relative-clauses')), Rule('sumti'), Or(Elidable(Terminal(LUhU), Optional(Repeated(Rule('free')))), Terminal(KOhA)), Or(Optional(Repeated(Rule('free'))), Rule('lerfu-string')), Or(Elidable(Terminal(BOI), Optional(Repeated(Rule('free')))), Terminal(LA)), Optional(Repeated(Rule('free'))), Optional(Rule('relative-clauses')), Repeated(Terminal(<class 'tokens.CMENE'>)), Or(Optional(Repeated(Rule('free'))), Paren(Or(Terminal(LA), Terminal(LE)))), Optional(Repeated(Rule('free'))), Rule('sumti-tail'), Or(Elidable(Terminal(KU), Optional(Repeated(Rule('free')))), Terminal(LI)), Optional(Repeated(Rule('free'))), Rule('mex'), Or(Elidable(Terminal(LOhO), Optional(Repeated(Rule('free')))), Terminal(ZO)), Rule('any-word'), Or(Optional(Repeated(Rule('free'))), Terminal(LU)), Rule('text'), Or(Elidable(Terminal(LIhU), Optional(Repeated(Rule('free')))), Terminal(LOhU)), Repeated(Rule('any-word')), Terminal(LEhU), Or(Optional(Repeated(Rule('free'))), Terminal(ZOI)), Rule('any-word'), Rule('anything'), Rule('any-word'), Optional(Repeated(Rule('free')))) ,\
  Rule('time-offset1033') :
     (Terminal(PU), Optional(Terminal(NAI)), Optional(Terminal(ZI))) ,\
  Rule('sumti-494') :
     (Or(Rule('sumti-5'), Rule('gek')), Rule('sumti'), Rule('gik'), Rule('sumti-4')) ,\
  Rule('tanru-unit-2152') :
     (Terminal(<class 'tokens.SELBRI'>), Or(Optional(Repeated(Rule('free'))), Terminal(GOhA)), Optional(Terminal(RAhO)), Or(Optional(Repeated(Rule('free'))), Terminal(KE)), Optional(Repeated(Rule('free'))), Rule('selbri-3'), Or(Elidable(Terminal(KEhE), Optional(Repeated(Rule('free')))), Terminal(ME)), Optional(Repeated(Rule('free'))), Rule('sumti'), Elidable(Terminal(MEhU), Optional(Repeated(Rule('free')))), Or(Optional(Terminal(MOI), Optional(Repeated(Rule('free')))), Paren(Or(Rule('number'), Rule('lerfu-string')))), Terminal(MOI), Or(Optional(Repeated(Rule('free'))), Terminal(NUhA)), Optional(Repeated(Rule('free'))), Or(Rule('mex-operator'), Terminal(SE)), Optional(Repeated(Rule('free'))), Or(Rule('tanru-unit-2'), Terminal(JAI)), Optional(Repeated(Rule('free'))), Optional(Rule('tag')), Or(Rule('tanru-unit-2'), Rule('any-word')), Or(Repeated(Paren(Terminal(ZEI), Rule('any-word'))), Terminal(NAhE)), Optional(Repeated(Rule('free'))), Or(Rule('tanru-unit-2'), Terminal(NU)), Optional(Terminal(NAI)), Optional(Repeated(Rule('free'))), Repeated(Optional(Rule('joik-jek'), Terminal(NU), Optional(Terminal(NAI)), Optional(Repeated(Rule('free'))))), Rule('subsentence'), Elidable(Terminal(KEI), Optional(Repeated(Rule('free'))))) ,\
  Rule('operator-2372') :
     (Or(Rule('mex-operator'), Terminal(KE)), Optional(Repeated(Rule('free'))), Rule('operator'), Elidable(Terminal(KEhE), Optional(Repeated(Rule('free'))))) ,\
  Rule('sentence40') :
     (Optional(Rule('terms'), Optional(Terminal(CU), Optional(Repeated(Rule('free'))))), Rule('bridi-tail')) ,\
  Rule('lerfu-word987') :
     (Or(Terminal(BY), Rule('any-word')), Or(Terminal(BU), Terminal(LAU)), Or(Rule('lerfu-word'), Terminal(TEI)), Rule('lerfu-string'), Terminal(FOI)) ,\
  Rule('selbri-2132') :
     (Rule('selbri-3'), Optional(Terminal(CO), Optional(Repeated(Rule('free'))), Rule('selbri-2'))) ,\
}
