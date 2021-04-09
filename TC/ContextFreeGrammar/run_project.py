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
grammar2.removeRec()
grammar3 = ContextFreeGrammar("S", ["S"], ["a", "b"], {"S":["S", "a", "b"]})
grammar3.removeRec()
# example of indirect left recursion
# A -> Br
# B -> Cd
# C -> At
grammar4 = ContextFreeGrammar("A", ["A","B","C"], ["r","d","t"],{"A":["Br"],"B":["Cd"],"C":["At"]})
grammar4.removeRec()
print(grammar4.production_rule)
# example for left factorize : S-> aA|aB|b
grammar5 = ContextFreeGrammar("S", ["S","A","B"], ["a","b"], {"S":["aA","aB","b"]})
grammar5.leftFactorize()
print(grammar5.production_rule)
