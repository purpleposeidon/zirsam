#!/usr/bin/environ python3


from magic_bnf import *
import sys; sys.path.append('../')
from tokens import *
from selmaho import *
from special_terminals import *


import bnf_data
from convert_bnf import head_info, tail_info, bnf #<-- if you want, uhm... try something else okay?

def fix(term):
    """
    Turn ((a+b)+c) into (a+(b+c))
    """
    if isinstance(term, Condition):
        rep = []
        for t in term.terms:
            rep.append(fix(t))
        term.terms = rep
        if len(term.terms) == 2:
            if type(term.terms[0]) == type(term.terms[1]) == type(term):
             taip = type(term)
             ab, c = term.terms
             a, b = term.terms
             bc = taip(b, c)
             return taip(a, bc)
    return term

def optimize(BNF):
    new_bnf = {}
    for key in bnf_data.BNF:
        new_bnf[key] = fix(bnf_data.BNF[key])
    return new_bnf

def main():
    b = optimize(bnf_data.BNF)
    print(head_info)
    print("BNF = {")
    for key in b:
        r = repr(b[key])
        if 0 and 'undermatch' in r:
            print(key, file=sys.stderr)
            print(type(key), file=sys.stderr)
            print(dir(key), file=sys.stderr)
            input()
            #raise Exception(str(r))
        r = r.replace("<class '", '').replace('<class "', '').replace("'>", '').replace('">', '')
        print("{0!r}:\n    {1},".format(key, r))
    print("}")
    print(tail_info)

if __name__ == '__main__':
    import bnf_data
    import sys
    sys.stdout = open(bnf, 'w')
    main()
