from itertools import combinations_with_replacement
import numpy as np
import string
from copy import deepcopy

cypher_text = "3CC85DD318D40EC809810EC05DC518C20FC80DD518DB148110C40EC017D411" 
len_cypher_text = len(cypher_text)
decypher_text = ""
key_len = 2
alphabet = string.ascii_lowercase + string.ascii_uppercase
possible_keys = []

"""
    In cazul nostru lungimea cheii este mai mica decat lungimea textului original, si deci vom avea o cheie circulara. In loc sa
    facem operatia de xor pentru toate posibilitatile de chei (in cazul nostru avem 2 litere, deci 52 x 52 = 2704 de posibilitati),
    incercam sa gasim o lista de posibile chei.
"""
def find_possible_keys(start):
    count_possible_keys = list([0] * 256)

    for i in range(start, len_cypher_text, 4):
        from_hexa = int("0x" + cypher_text[i:i+2], base=16)

        for k in range(0, 256):
            for l in alphabet:
                if from_hexa == k ^ ord(l):
                    count_possible_keys[k] += 1

    possible_keys.append(np.argwhere(count_possible_keys == np.amax(count_possible_keys)).flatten().tolist())


indexes = list(range(0,2*key_len,2))

for ind in indexes:
    find_possible_keys(ind)

print(possible_keys)

for fst in possible_keys[0]:
    for snd in possible_keys[1]:
        cypher_text_copy = deepcopy(cypher_text)
        for i in range(0, len(cypher_text), 2): # fiecare litera a mesajului original este reprezentat de 2 caractere in hexa
            if i % 4 == 2:
                litera = chr( snd ^ (int("0x" + cypher_text_copy[i:i+2], base=16)) )
            else:
                litera = chr ( fst ^ (int("0x" + cypher_text_copy[i:i+2], base=16)) )
            decypher_text += litera

        print(decypher_text, "   ", "(", fst, ", ", snd, ")"  )
        print()
        decypher_text = ""
    
# R: Ai reusit sa decriptezi mesajul     ( 125 ,  161 )