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
# example of indirect left recursion
grammar4 = ContextFreeGrammar("A", ["A","B","C"], ["r","d","t"],{"A":["Br"],"B":["Cd"],"C":["At"]})
# example for left factorize : S->aA|aB
grammar5 = ContextFreeGrammar("S", ["S","A","B"], ["a","b"], {"S":["aA","aB","b"]})
grammar5.leftFactorize()
print(grammar5.production_rule)

# grammar3.removeRec()
# print(grammar3.production_rule)


