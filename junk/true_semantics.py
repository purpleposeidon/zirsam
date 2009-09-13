# -*- coding: utf-8 -*-

'''
So... you need a way to terminate symbols? What? Uhm....


Grab it by the terminator?

Need a way of checking that something is present.

No "if" allowed?





LE SELBRI <Some kind of terminator> SELBRI

lo nu mi nelci do cu nelci

lo nu mi nelci do kei nelci

lo nu mi tavla do <A Terminator Goes Here> nelci




def selmaho(parse_tree, token_stream):


def LE(parse_tree, token_stream):



Identify the selma'o of the current token
Token.selmaho.feed()

The Parse Tree interface
.up()
  - go to the root of the tree
.down()
  - enter a node
.nodes()
  - list the nodes

.i
    tavla
    [mi] [zo'e] [zoi zoi parsers zoi] [la
                        lojban
                      ]
.i
    ni'o
        ni'o
            .i
                klama
                    [la
                        alis
                    ] [lo
                        zarci
                      ]
            .i
                nelci
                    na
                    [lo
                        go'i
                    ] [lo
                        go'i
                            se
                      ]
        ni'o
            .i


class Node
    def __init__(self, parent=None)
        self.parent = parent
        self.children = []
        self.properties = {}
        self.terminator = None


root = Node()
if "i" or "ni'o":
    Consume()

i
'''


def main():
    root = Root()
    root.Parse(token_stream)

class Node:
    grammar = {}
    def __init__(self, init=None, parent=None):
        self.init = init
        self.children = []

    def child(self, node_type):
        kid = node_type(init=node_type.pop(), parent=self)
        self.children.append(kid)
        return kid.Parse(token_stream)

    def Parse(token_stream):
        t = token_stream[0]
        if t in self.grammar:
            token_stream.pop(0)
            child_type, *my_terminators = self.grammar[t] #Another py3k!
            c = self.child(child_type, token_stream)
            if c in my_terminators:
                return
            else:
                return c
        else:
            return t


class Root(Node):
    def Parse(token_stream):
        c = self.child(Section, token_stream)
        if c == FAhO:
            return
        raise ParserError("Could not handle token {0}".format(c))

class Section(Node):
    grammar = {I:(Sentence, I), NIhO:(Section)}



rules = {}
def Rule(name, **grammar):
    """
    Defines a new node type
    How to call the function:
        Rule("rule_name", this_token='next_rule')
    The rule will be added to the rules dictionary.

    Strings are 
    """
    for g in grammar:
      if type(grammar[g]) == str:
        grammar[g] = [grammar[g]]
    r = type(name, (Node,), grammar)
    rules[name] = r

def finalize_rules():
  #Convert strings to objects
  new_rules = {}
  for key in rules:
    new_grammar = {}
    for g in grammar:
      for subsection
    if type(key) == str:
      eval(key)


"""
Form:
  'rule' - Consume the token and call rule
  '.variable' - Append the Token to the node's list named "variable"
  'rule.variable' - Call "rule", and append it to "variable"
  '?rule' - Don't consume the token; it is given to the child
  '@' - It terminates this Node. But wouldn't it be better to have it handled by mom?
    - Why make mom do all the work? Surely the Rule is the best qualified to deal with this. Otherwise, there'd have to be extra stuff for mom to take care of. So, yes, use it.
  '-' - Terminate, but don't consume
* Get rid of that tuple-using code!

"""

Rule("section", I='sentence', NIhO='section')
Rule("sentence", DOI='vocative')
Rule("vocative", DOhU='@', CMENE='.target', selbri='.target')
Rule("bridi", SELBRI='.selbri', sumti='.sumti')
Rule("sumti", LE='.referrent')


rules = finalize_rules()