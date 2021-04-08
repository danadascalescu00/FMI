from helpers import *

class ContextFreeGrammar:
    def __init__(self, start, nonterminals=[], terminals=[], production_rule={}, lambda_sym="ł"):
        self.start = start
        self.nonterminals = nonterminals
        self.terminals = terminals
        self.production_rule = production_rule
        self._lambda = lambda_sym


    def removeDirectLeftRec(self, nonterminal):
        rep_production, new_production = [], []
        # introduce new nonterminal which will be write at the last of every terminal
        new_nonterminal = nonterminal + "'"

        for prod in self.production_rule[nonterminal]:
            if nonterminal == prod[0]:
                new_production.append(prod[1:] + nonterminal)
            else:
                rep_production.append(prod + new_nonterminal)

        if len(self.production_rule[nonterminal]) == 1: 
            rep_production = [new_nonterminal]
        new_production.insert(0,"?")
        self.production_rule[nonterminal] = rep_production
        self.production_rule[new_nonterminal] = new_production
        self.nonterminals.append(new_nonterminal)


    def checkIndirectLeftRec(self, nonterminal1, nonterminal2):
        if nonterminal1 == nonterminal2:
            return True
        else:
            for prod in self.production_rule[nonterminal2]:
                if prod[0] in self.nonterminals:
                    return self.checkIndirectLeftRec(nonterminal1, prod[0])

        return False


    def removeIndirectLeftRec(self, nonterminal, nonterminal_order):
        for pos, nonterminal2 in enumerate(list(self.production_rule)):
            if nonterminal != nonterminal2 and pos > nonterminal_order:
                for idx, prod in enumerate(self.production_rule[nonterminal2]):
                    if prod[0] == nonterminal:
                        rep_production = ''.join([str(elem) + ('|' if elem != self.production_rule[nonterminal][-1] else '') for elem in self.production_rule[nonterminal]])
                        self.production_rule[nonterminal2][idx] =  rep_production + self.production_rule[nonterminal2][idx][1:]


    def removeRec(self):
        # identify if any production causes indirect left recursion
        for pos, nonterminal in enumerate(list(self.production_rule)):
            for rule in self.production_rule[nonterminal]:
                symbol = rule[0]
                if (nonterminal != symbol) and (symbol in self.nonterminals): 
                    if self.checkIndirectLeftRec(nonterminal,symbol):
                        self.removeIndirectLeftRec(nonterminal, pos)

        # removal of direct left recursion
        for nonterminal in list(self.production_rule):
            if any(nonterminal == r[0] for r in self.production_rule[nonterminal]):
                self.removeDirectLeftRec(nonterminal)


    def leftFactorize(self):
        prefixes = []

        for nonterminal in list(self.production_rule):
            rules = self.production_rule[nonterminal]
            if len(rules) == 1:
                continue

            # we check for each nonterminal if there is a non-trivial prefix 
            nontrivial_prefixes = nonTrivialPrefixes(rules)
            if not nontrivial_prefixes:
                continue

            for prefix, rule in nontrivial_prefixes.items():
                commons = [c[0] for c in takewhile(same_prefix,zip(*rule))]
                prefixes.append(''.join(commons))

            for prefix in prefixes:
                new_production = []
                new_nonterminal = alphabet.pop() + "'"                
                while new_nonterminal in self.nonterminals:
                    new_nonterminal = alphabet.pop() + "'"
                self.nonterminals.append(new_nonterminal)

                for r in self.production_rule[nonterminal]:
                    if r.startswith(prefix):
                        r = r.replace(prefix,"",1)
                        new_production.append(r)

                for r in nontrivial_prefixes[prefix]:
                    self.production_rule[nonterminal].remove(r)

                self.production_rule[nonterminal].append(prefix + new_nonterminal)
                self.production_rule[new_nonterminal] = new_production