# -*- coding: utf-8 -*-

"""
The comment below contains code to generate a functions for everything.
First the pre_handle function is called. Then the functions for the sub-nodes are called.
Then the end_handle function is called.
"tracker" is a dendrography.MatchTracker object, context is semantics.foo.Context

It might be better to, instead of having ALL of those MANY empty functions, to just test to see if the function is  listed in the dictionary, or something. Maybe check for presence in a module, or something.
"""
'''
out = open("/tmp/tracker_boiler.py", 'w')
import bnf
used = []
for rule in bnf.BNF.keys():
  if type(rule) == str or rule.name[0] == 'x':
    continue
  print("""
def pre_handle_{0}(tracker, context): pass
def end_handle_{0}(tracker, context): pass""".format(str(rule)), file=out)
  used.append(rule.name)

print("\n\nhandlers = {", file=out)
for rule in used:
  print("  'pre_{0}': pre_handle_{0},".format(rule), file=out)
  print("  'end_{0}': end_handle_{0},".format(rule), file=out)

print("}", file=out)
out.close()

'''

"""
Okay, here's what's going down...
We need a function for TERM. It adds the place to an empty shell-thing...
We'll need a few functions for... sentence, tanru_unit. But let's do one thing at a time.
ko'a broda ko'e ko'i ko'o ko'u
fa ko'a broda fe ko'e fi ko'i fo ko'o fu ko'u

lo broda cu brode lo brodi lo brodo lo brodu
ko'a broda be ko'e bei ko'i be'o ko'u
lo broda be ko'e be'o cu brode

la djan goi ko'a cu barda .i ko'a mlatu
"""

import sys
#sys.path.append('./')
import dendrography
import selmaho
sys.path.append("./semantology")
import semantology

class SemanticsException(Exception): pass

def examine(tracker, context):
  
  handlers.get('pre_'+tracker.rule.name, void_handler)(tracker, context)
  for value in tracker.value:
    if isinstance(value, dendrography.MatchTracker):
      examine(value, context)
  handlers.get('end_'+tracker.rule.name, void_handler)(tracker, context)

def void_handler(tracker, context): pass

#--------------- boiler-plate goes here ---------------

def pre_handle_sentence(tracker, context):
  context.push_abstraction()
def end_handle_sentence(tracker, context):
  context.pop_abstraction()

def pre_handle_text(tracker, context): pass
def end_handle_text(tracker, context): pass

def pre_handle_subsentence(tracker, context): pass
def end_handle_subsentence(tracker, context): pass

def pre_handle_relative_clause(tracker, context): pass
def end_handle_relative_clause(tracker, context): pass

def pre_handle_indicator(tracker, context): pass
def end_handle_indicator(tracker, context): pass

def pre_handle_sumti_tail_1(tracker, context): pass
def end_handle_sumti_tail_1(tracker, context): pass

def pre_handle_tanru_unit_2(tracker, context):
  selbri = tracker.node.get("SELBRI")
  if not selbri:
    raise SemanticsException("Can only handle SELBRI right now, but tanru_unit_2 consists of {0}".format(tracker.node))
  context.abstraction_stack[0].selbri.insert(0, selbri)
def end_handle_tanru_unit_2(tracker, context): pass

def pre_handle_tanru_unit_1(tracker, context): pass
def end_handle_tanru_unit_1(tracker, context): pass

def pre_handle_operator_2(tracker, context): pass
def end_handle_operator_2(tracker, context): pass

def pre_handle_operator_1(tracker, context): pass
def end_handle_operator_1(tracker, context): pass

def pre_handle_mex_2(tracker, context): pass
def end_handle_mex_2(tracker, context): pass

def pre_handle_bridi_tail(tracker, context):
  obs = context.abstraction_stack[-1].observative
  if obs == ...:
    context.abstraction_stack[-1].observative = True
def end_handle_bridi_tail(tracker, context): pass

def pre_handle_termset(tracker, context): pass
def end_handle_termset(tracker, context): pass

def pre_handle_fragment(tracker, context): pass
def end_handle_fragment(tracker, context): pass

def pre_handle_selbri(tracker, context): pass
def end_handle_selbri(tracker, context): pass

def pre_handle_b(tracker, context): pass
def end_handle_b(tracker, context): pass

def pre_handle_sumti_tail(tracker, context): pass
def end_handle_sumti_tail(tracker, context): pass

def pre_handle_gek(tracker, context): pass
def end_handle_gek(tracker, context): pass

def pre_handle_quantifier(tracker, context): pass
def end_handle_quantifier(tracker, context): pass

def pre_handle_term(tracker, context):
  FA = tracker.node.get("FA")
  if FA:
    FA = selmaho.FA.forms.index(FA.value)
  term_num = context.abstraction_stack[-1].next_term(FA)
  new_term = semantology.Terbri(context.abstraction_stack[-1], term_num, "nei", ...)
  context.abstraction_stack[-1].terms.append(new_term)
  
def end_handle_term(tracker, context): pass

def pre_handle_rp_operand(tracker, context): pass
def end_handle_rp_operand(tracker, context): pass

def pre_handle_tanru_unit(tracker, context): pass
def end_handle_tanru_unit(tracker, context): pass

def pre_handle_ek(tracker, context): pass
def end_handle_ek(tracker, context): pass

def pre_handle_paragraphs(tracker, context): pass
def end_handle_paragraphs(tracker, context): pass

def pre_handle_operand(tracker, context): pass
def end_handle_operand(tracker, context): pass

def pre_handle_bridi_tail_1(tracker, context): pass
def end_handle_bridi_tail_1(tracker, context): pass

def pre_handle_bridi_tail_2(tracker, context): pass
def end_handle_bridi_tail_2(tracker, context): pass

def pre_handle_bridi_tail_3(tracker, context): pass
def end_handle_bridi_tail_3(tracker, context): pass

def pre_handle_space(tracker, context): pass
def end_handle_space(tracker, context): pass

def pre_handle_rp_expression(tracker, context): pass
def end_handle_rp_expression(tracker, context): pass

def pre_handle_paragraph(tracker, context): pass
def end_handle_paragraph(tracker, context): pass

def pre_handle_sumti(tracker, context): pass
def end_handle_sumti(tracker, context): pass

def pre_handle_terms(tracker, context): pass
def end_handle_terms(tracker, context): pass

def pre_handle_free(tracker, context): pass
def end_handle_free(tracker, context): pass

def pre_handle_gihek(tracker, context): pass
def end_handle_gihek(tracker, context): pass

def pre_handle_time_offset(tracker, context): pass
def end_handle_time_offset(tracker, context): pass

def pre_handle_relative_clauses(tracker, context): pass
def end_handle_relative_clauses(tracker, context): pass

def pre_handle_number(tracker, context): pass
def end_handle_number(tracker, context): pass

def pre_handle_operator(tracker, context): pass
def end_handle_operator(tracker, context): pass

def pre_handle_statement_1(tracker, context): pass
def end_handle_statement_1(tracker, context): pass

def pre_handle_mex(tracker, context): pass
def end_handle_mex(tracker, context): pass

def pre_handle_space_int_props(tracker, context): pass
def end_handle_space_int_props(tracker, context): pass

def pre_handle_statement(tracker, context): pass
def end_handle_statement(tracker, context): pass

def pre_handle_indicators(tracker, context): pass
def end_handle_indicators(tracker, context): pass

def pre_handle_jek(tracker, context): pass
def end_handle_jek(tracker, context): pass

def pre_handle_gik(tracker, context): pass
def end_handle_gik(tracker, context): pass

def pre_handle_joik_jek(tracker, context): pass
def end_handle_joik_jek(tracker, context): pass

def pre_handle_selbri_1(tracker, context): pass
def end_handle_selbri_1(tracker, context): pass

def pre_handle_selbri_2(tracker, context): pass
def end_handle_selbri_2(tracker, context): pass

def pre_handle_selbri_3(tracker, context): pass
def end_handle_selbri_3(tracker, context): pass

def pre_handle_selbri_4(tracker, context): pass
def end_handle_selbri_4(tracker, context): pass

def pre_handle_selbri_5(tracker, context): pass
def end_handle_selbri_5(tracker, context): pass

def pre_handle_selbri_6(tracker, context): pass
def end_handle_selbri_6(tracker, context): pass

def pre_handle_guhek(tracker, context): pass
def end_handle_guhek(tracker, context): pass

def pre_handle_joik(tracker, context): pass
def end_handle_joik(tracker, context): pass

def pre_handle_mex_1(tracker, context): pass
def end_handle_mex_1(tracker, context): pass

def pre_handle_lerfu_word(tracker, context): pass
def end_handle_lerfu_word(tracker, context): pass

def pre_handle_joik_ek(tracker, context): pass
def end_handle_joik_ek(tracker, context): pass

def pre_handle_interval_property(tracker, context): pass
def end_handle_interval_property(tracker, context): pass

def pre_handle_space_offset(tracker, context): pass
def end_handle_space_offset(tracker, context): pass

def pre_handle_links(tracker, context): pass
def end_handle_links(tracker, context): pass

def pre_handle_space_interval(tracker, context): pass
def end_handle_space_interval(tracker, context): pass

def pre_handle_prenex(tracker, context): pass
def end_handle_prenex(tracker, context): pass

def pre_handle_tag(tracker, context): pass
def end_handle_tag(tracker, context): pass

def pre_handle_linkargs(tracker, context): pass
def end_handle_linkargs(tracker, context): pass

def pre_handle_text_1(tracker, context): pass
def end_handle_text_1(tracker, context): pass

def pre_handle_gek_sentence(tracker, context): pass
def end_handle_gek_sentence(tracker, context): pass

def pre_handle_terms_1(tracker, context): pass
def end_handle_terms_1(tracker, context): pass

def pre_handle_mex_operator(tracker, context): pass
def end_handle_mex_operator(tracker, context): pass

def pre_handle_simple_tense_modal(tracker, context): pass
def end_handle_simple_tense_modal(tracker, context): pass

def pre_handle_vocative(tracker, context): pass
def end_handle_vocative(tracker, context): pass

def pre_handle_terms_2(tracker, context): pass
def end_handle_terms_2(tracker, context): pass

def pre_handle_sumti_6(tracker, context):
  context.abstraction_stack[-1].terms[-1].sumti = tracker.value[0]
  
def end_handle_sumti_6(tracker, context): pass

def pre_handle_sumti_4(tracker, context): pass
def end_handle_sumti_4(tracker, context): pass

def pre_handle_sumti_5(tracker, context): pass
def end_handle_sumti_5(tracker, context): pass

def pre_handle_sumti_2(tracker, context): pass
def end_handle_sumti_2(tracker, context): pass

def pre_handle_sumti_3(tracker, context): pass
def end_handle_sumti_3(tracker, context): pass

def pre_handle_lerfu_string(tracker, context): pass
def end_handle_lerfu_string(tracker, context): pass

def pre_handle_sumti_1(tracker, context): pass
def end_handle_sumti_1(tracker, context): pass

def pre_handle_stag(tracker, context): pass
def end_handle_stag(tracker, context): pass

def pre_handle_tail_terms(tracker, context): pass
def end_handle_tail_terms(tracker, context): pass

def pre_handle_tense_modal(tracker, context): pass
def end_handle_tense_modal(tracker, context): pass

def pre_handle_statement_3(tracker, context): pass
def end_handle_statement_3(tracker, context): pass

def pre_handle_statement_2(tracker, context): pass
def end_handle_statement_2(tracker, context): pass

def pre_handle_a(tracker, context): pass
def end_handle_a(tracker, context): pass

def pre_handle_interval(tracker, context): pass
def end_handle_interval(tracker, context): pass

def pre_handle_time(tracker, context): pass
def end_handle_time(tracker, context): pass

def pre_handle_operand_3(tracker, context): pass
def end_handle_operand_3(tracker, context): pass

def pre_handle_operand_2(tracker, context): pass
def end_handle_operand_2(tracker, context): pass

def pre_handle_operand_1(tracker, context): pass
def end_handle_operand_1(tracker, context): pass


handlers = {
  'pre_sentence': pre_handle_sentence,
  'end_sentence': end_handle_sentence,
  'pre_text': pre_handle_text,
  'end_text': end_handle_text,
  'pre_subsentence': pre_handle_subsentence,
  'end_subsentence': end_handle_subsentence,
  'pre_relative_clause': pre_handle_relative_clause,
  'end_relative_clause': end_handle_relative_clause,
  'pre_indicator': pre_handle_indicator,
  'end_indicator': end_handle_indicator,
  'pre_sumti_tail_1': pre_handle_sumti_tail_1,
  'end_sumti_tail_1': end_handle_sumti_tail_1,
  'pre_tanru_unit_2': pre_handle_tanru_unit_2,
  'end_tanru_unit_2': end_handle_tanru_unit_2,
  'pre_tanru_unit_1': pre_handle_tanru_unit_1,
  'end_tanru_unit_1': end_handle_tanru_unit_1,
  'pre_operator_2': pre_handle_operator_2,
  'end_operator_2': end_handle_operator_2,
  'pre_operator_1': pre_handle_operator_1,
  'end_operator_1': end_handle_operator_1,
  'pre_mex_2': pre_handle_mex_2,
  'end_mex_2': end_handle_mex_2,
  'pre_bridi_tail': pre_handle_bridi_tail,
  'end_bridi_tail': end_handle_bridi_tail,
  'pre_termset': pre_handle_termset,
  'end_termset': end_handle_termset,
  'pre_fragment': pre_handle_fragment,
  'end_fragment': end_handle_fragment,
  'pre_selbri': pre_handle_selbri,
  'end_selbri': end_handle_selbri,
  'pre_b': pre_handle_b,
  'end_b': end_handle_b,
  'pre_sumti_tail': pre_handle_sumti_tail,
  'end_sumti_tail': end_handle_sumti_tail,
  'pre_gek': pre_handle_gek,
  'end_gek': end_handle_gek,
  'pre_quantifier': pre_handle_quantifier,
  'end_quantifier': end_handle_quantifier,
  'pre_term': pre_handle_term,
  'end_term': end_handle_term,
  'pre_rp_operand': pre_handle_rp_operand,
  'end_rp_operand': end_handle_rp_operand,
  'pre_tanru_unit': pre_handle_tanru_unit,
  'end_tanru_unit': end_handle_tanru_unit,
  'pre_ek': pre_handle_ek,
  'end_ek': end_handle_ek,
  'pre_paragraphs': pre_handle_paragraphs,
  'end_paragraphs': end_handle_paragraphs,
  'pre_operand': pre_handle_operand,
  'end_operand': end_handle_operand,
  'pre_bridi_tail_1': pre_handle_bridi_tail_1,
  'end_bridi_tail_1': end_handle_bridi_tail_1,
  'pre_bridi_tail_2': pre_handle_bridi_tail_2,
  'end_bridi_tail_2': end_handle_bridi_tail_2,
  'pre_bridi_tail_3': pre_handle_bridi_tail_3,
  'end_bridi_tail_3': end_handle_bridi_tail_3,
  'pre_space': pre_handle_space,
  'end_space': end_handle_space,
  'pre_rp_expression': pre_handle_rp_expression,
  'end_rp_expression': end_handle_rp_expression,
  'pre_paragraph': pre_handle_paragraph,
  'end_paragraph': end_handle_paragraph,
  'pre_sumti': pre_handle_sumti,
  'end_sumti': end_handle_sumti,
  'pre_terms': pre_handle_terms,
  'end_terms': end_handle_terms,
  'pre_free': pre_handle_free,
  'end_free': end_handle_free,
  'pre_gihek': pre_handle_gihek,
  'end_gihek': end_handle_gihek,
  'pre_time_offset': pre_handle_time_offset,
  'end_time_offset': end_handle_time_offset,
  'pre_relative_clauses': pre_handle_relative_clauses,
  'end_relative_clauses': end_handle_relative_clauses,
  'pre_number': pre_handle_number,
  'end_number': end_handle_number,
  'pre_operator': pre_handle_operator,
  'end_operator': end_handle_operator,
  'pre_statement_1': pre_handle_statement_1,
  'end_statement_1': end_handle_statement_1,
  'pre_mex': pre_handle_mex,
  'end_mex': end_handle_mex,
  'pre_space_int_props': pre_handle_space_int_props,
  'end_space_int_props': end_handle_space_int_props,
  'pre_statement': pre_handle_statement,
  'end_statement': end_handle_statement,
  'pre_indicators': pre_handle_indicators,
  'end_indicators': end_handle_indicators,
  'pre_jek': pre_handle_jek,
  'end_jek': end_handle_jek,
  'pre_gik': pre_handle_gik,
  'end_gik': end_handle_gik,
  'pre_joik_jek': pre_handle_joik_jek,
  'end_joik_jek': end_handle_joik_jek,
  'pre_selbri_1': pre_handle_selbri_1,
  'end_selbri_1': end_handle_selbri_1,
  'pre_selbri_2': pre_handle_selbri_2,
  'end_selbri_2': end_handle_selbri_2,
  'pre_selbri_3': pre_handle_selbri_3,
  'end_selbri_3': end_handle_selbri_3,
  'pre_selbri_4': pre_handle_selbri_4,
  'end_selbri_4': end_handle_selbri_4,
  'pre_selbri_5': pre_handle_selbri_5,
  'end_selbri_5': end_handle_selbri_5,
  'pre_selbri_6': pre_handle_selbri_6,
  'end_selbri_6': end_handle_selbri_6,
  'pre_guhek': pre_handle_guhek,
  'end_guhek': end_handle_guhek,
  'pre_joik': pre_handle_joik,
  'end_joik': end_handle_joik,
  'pre_mex_1': pre_handle_mex_1,
  'end_mex_1': end_handle_mex_1,
  'pre_lerfu_word': pre_handle_lerfu_word,
  'end_lerfu_word': end_handle_lerfu_word,
  'pre_joik_ek': pre_handle_joik_ek,
  'end_joik_ek': end_handle_joik_ek,
  'pre_interval_property': pre_handle_interval_property,
  'end_interval_property': end_handle_interval_property,
  'pre_space_offset': pre_handle_space_offset,
  'end_space_offset': end_handle_space_offset,
  'pre_links': pre_handle_links,
  'end_links': end_handle_links,
  'pre_space_interval': pre_handle_space_interval,
  'end_space_interval': end_handle_space_interval,
  'pre_prenex': pre_handle_prenex,
  'end_prenex': end_handle_prenex,
  'pre_tag': pre_handle_tag,
  'end_tag': end_handle_tag,
  'pre_linkargs': pre_handle_linkargs,
  'end_linkargs': end_handle_linkargs,
  'pre_text_1': pre_handle_text_1,
  'end_text_1': end_handle_text_1,
  'pre_gek_sentence': pre_handle_gek_sentence,
  'end_gek_sentence': end_handle_gek_sentence,
  'pre_terms_1': pre_handle_terms_1,
  'end_terms_1': end_handle_terms_1,
  'pre_mex_operator': pre_handle_mex_operator,
  'end_mex_operator': end_handle_mex_operator,
  'pre_simple_tense_modal': pre_handle_simple_tense_modal,
  'end_simple_tense_modal': end_handle_simple_tense_modal,
  'pre_vocative': pre_handle_vocative,
  'end_vocative': end_handle_vocative,
  'pre_terms_2': pre_handle_terms_2,
  'end_terms_2': end_handle_terms_2,
  'pre_sumti_6': pre_handle_sumti_6,
  'end_sumti_6': end_handle_sumti_6,
  'pre_sumti_4': pre_handle_sumti_4,
  'end_sumti_4': end_handle_sumti_4,
  'pre_sumti_5': pre_handle_sumti_5,
  'end_sumti_5': end_handle_sumti_5,
  'pre_sumti_2': pre_handle_sumti_2,
  'end_sumti_2': end_handle_sumti_2,
  'pre_sumti_3': pre_handle_sumti_3,
  'end_sumti_3': end_handle_sumti_3,
  'pre_lerfu_string': pre_handle_lerfu_string,
  'end_lerfu_string': end_handle_lerfu_string,
  'pre_sumti_1': pre_handle_sumti_1,
  'end_sumti_1': end_handle_sumti_1,
  'pre_stag': pre_handle_stag,
  'end_stag': end_handle_stag,
  'pre_tail_terms': pre_handle_tail_terms,
  'end_tail_terms': end_handle_tail_terms,
  'pre_tense_modal': pre_handle_tense_modal,
  'end_tense_modal': end_handle_tense_modal,
  'pre_statement_3': pre_handle_statement_3,
  'end_statement_3': end_handle_statement_3,
  'pre_statement_2': pre_handle_statement_2,
  'end_statement_2': end_handle_statement_2,
  'pre_a': pre_handle_a,
  'end_a': end_handle_a,
  'pre_interval': pre_handle_interval,
  'end_interval': end_handle_interval,
  'pre_time': pre_handle_time,
  'end_time': end_handle_time,
  'pre_operand_3': pre_handle_operand_3,
  'end_operand_3': end_handle_operand_3,
  'pre_operand_2': pre_handle_operand_2,
  'end_operand_2': end_handle_operand_2,
  'pre_operand_1': pre_handle_operand_1,
  'end_operand_1': end_handle_operand_1,
}
