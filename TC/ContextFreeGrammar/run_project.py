from ContexFreeGrammar import *

start = "E"
lambda_var = "ł"
neterminali = ["E", "D", "T", "W", "F"]
terminali = ["a", "(", ")", lambda_var, "*", "+"]
productii = {
    "E": ["TD"],
    "D": ["+TD", lambda_var],
    "T": ["FW"],
    "W": ["*FW", lambda_var],
    "F": ["(E)", "a"]
}

grammar1 = ContextFreeGrammar(start, neterminali, terminali, productii)
# examples of direct left recursion
grammar2 = ContextFreeGrammar("A", ["A"], ["a", "b", "c", "d"], {"A":["Aa", "Ab", "c", "d"]})
grammar3 = ContextFreeGrammar("S", ["S"], ["a", "b"], {"S":["S", "a", "b"]})
# example od indirect left recursion
grammar4 = ContextFreeGrammar("A", ["A","B","C"], ["r","d","t"],{"A":["Br"],"B":["Cd"],"C":["At"]})

grammar3.removeRec()
print(grammar3.production_rule)


