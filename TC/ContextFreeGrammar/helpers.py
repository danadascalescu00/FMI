from string import ascii_uppercase
from itertools import takewhile

alphabet = list(ascii_uppercase)
alphabet.reverse()

def same_prefix(characters):
    return len(set(characters)) == 1


def nonTrivialPrefixes(rules):
    groups = {}
    initials = list(set([symbols[0] for symbols in rules]))
    previous, current = None, None
    previous_rule = ""

    for symbol in initials:
        current = symbol
        for rule in rules:
            if rule.startswith(symbol):
                if previous == None or previous != current: # first time when we find the symbol
                    previous = current
                    previous_rule = rule
                else:
                    if symbol not in groups:
                        groups[symbol] = []
                    groups[symbol].append(previous_rule)
                    groups[symbol].append(rule)

    return groups