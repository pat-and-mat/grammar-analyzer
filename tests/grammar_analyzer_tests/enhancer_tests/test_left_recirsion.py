from pycmp.grammar import Grammar
from grammar_analyzer.enhancer.left_recursion import general_recursion_eliminate, __direct_recursion_eliminate, epsilon_productions_eliminate
from grammar_analyzer.enhancer.converter import graph_to_grammar, grammar_to_graph

################################################################################################################
# epsilon test #1
grammar = Grammar()
S = grammar.add_nonterminal("S", True)
A, B, C = grammar.add_nonterminals("A B C")
a, b = grammar.add_terminals("a b")

S %= A + B
S %= C

A %= b + A + b
A %= grammar.epsilon

B %= b

C %= a
C %= b

new_grammar = epsilon_productions_eliminate(grammar)

_, new_grammar = grammar_to_graph(new_grammar)

_graph = {}
_graph["S"] = [["A", "B"], ["C"], ["B"]]
_graph["A"] = [["b", "A", "b"], ["b", "b"]]
_graph["B"] = [["b"]]
_graph["C"] = [["a"], ["b"]]

assert (new_grammar == _graph)

##############################################################################################################
# epsilon test #2

grammar = Grammar()
S = grammar.add_nonterminal("S", True)
A, B, C = grammar.add_nonterminals("A B C")
a, b = grammar.add_terminals("a b")

S %= A + B
S %= C

A %= b + A + b
A %= grammar.epsilon

B %= b
B %= grammar.epsilon

C %= a
C %= b

new_grammar = epsilon_productions_eliminate(grammar)

_, new_grammar = grammar_to_graph(new_grammar)

_graph = {}
_graph["S"] = [["A", "B"], ["C"], ["B"], ["A"], []]
_graph["A"] = [["b", "A", "b"], ["b", "b"]]
_graph["B"] = [["b"]]
_graph["C"] = [["a"], ["b"]]

assert (new_grammar == _graph)

##############################################################################################################
# direct test #1

grammar = Grammar()
S = grammar.add_nonterminal("S", True)
A, B, C = grammar.add_nonterminals("A B C")
a, b = grammar.add_terminals("a b")

S %= A + B
S %= C

A %= A + b
A %= a

B %= b

C %= a
C %= b

_, G = grammar_to_graph(grammar)
new_grammar = __direct_recursion_eliminate(G)

_graph = {}
_graph["S"] = [["A", "B"], ["C"]]
_graph["A"] = [["a", "A'"]]
_graph["A'"] = [["b", "A'"], []]
_graph["B"] = [["b"]]
_graph["C"] = [["a"], ["b"]]

assert (new_grammar == _graph)

##############################################################################################################
# general test #1

grammar = Grammar()
S = grammar.add_nonterminal("S", True)
A, B, C = grammar.add_nonterminals("A B C")
a, b = grammar.add_terminals("a b")

S %= A + b
S %= C

A %= B + a

B %= S + b

C %= b

new_grammar = general_recursion_eliminate(grammar)
_, new_grammar = grammar_to_graph(new_grammar)

_graph = {}
_graph["S"] = [["A", "b"], ["C"]]
_graph["A"] = [["B", "a"]]
_graph["B"] = [["C", "b", "B'"]]
_graph["B'"] = [["a", "b", "b", "B'"], []]
_graph["C"] = [["b"]]

print(_graph)
print(new_grammar)

assert (new_grammar == _graph)