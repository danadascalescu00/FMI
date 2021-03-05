"""
    De ce castiga mereu casele de pariuri? Jocul consista in a pune pariu pe jetonul ce urmeaza sa fie extras dintr-o punga 
    ce contine jetoane de la 1 la 100. 
    Regulile jocului:
        Jucatorul pune pariu ori pe un numar impar ori pe un numar par. Jetoanele cu numerele 13, 99, 100  sunt jetoane speciale.
        Daca se pariaza pentru un numar par si obtinem jetonul numarul 100, atunci jucatorul pierde. Daca se pariaza pentru un numar
        impar si jucatorul obtine jetonul cu numarul 99, atunci jucatorul pierde. Daca din punga este extras jetonul cu numarul 13,
        jucatorul pierde indiferent de paritatea numarului.

    De la 1 la 100 sunt 50 de numere pare, respectiv 50 de numere impare. 
    Probabilitatea de a castiga daca se pariaza pe numere impare este 48/100, respectiv 49/100 daca se pariaza pe numere pare.
    Cota casei, adica castigul care ii revine pentru fiecare pariu, este de (52 - 48) / 100 = 4% pentru numere impare, respectiv
    (51 - 49) / 100 = 2% pentru numere pare.
    In concluzie pentru fiecare 1$ pariat, 0.02$ sau 0.04$ se duc spre casa. De asemenea, sansa de castig este mai mare daca 
    pariem pe numere pare.
"""

import random
import locale
from sys import exit
from random import randint
from copy import deepcopy
import matplotlib.pyplot as plt


# Jucatorul poate alege daca pariaza pe numere pare sau impare
choice = input("Do you want to bet on Even or Odd numbers? \nE/O: ")

def play():
    token = randint(1,100)

    if token == 13:
        return False

    if choice.upper() == "E":
        if token % 2 or token  == 100:
            return False
        return True
    elif choice.upper() == 'O':
        if token % 2 == 0 or token == 99:
            return False
        return True
    else:
        print("Wrong choice!")
        exit(1)


def simulation(amount, bet, num_plays, ending_funds):
    number_of_plays, money = [], []

    for ind_play in range(1,num_plays+1):
        if play() == True:
            # Jucatorul a castigat
            amount = amount + bet
        else:
            # Jucatorul a pierdut
            amount = amount - bet
        number_of_plays.append(ind_play)
        money.append(amount)

    plt.ylabel('Player\'s amount in $')
    plt.xlabel('Number of bets')
    plt.plot(number_of_plays,money)

    ending_funds.append(money[-1])
    return money[-1]

start_amount = int(input("Amount of money you will start the game: "))
bet_amount = int(input("The amount you bet on: "))
print()
number_of_bets = 75

ending_funds, amount_of_money_left, money_start = [], 0, deepcopy(start_amount)
for i in range(100): # numarul simularilor
    amount_of_money_left = simulation(start_amount,bet_amount,number_of_bets,ending_funds)
    print("Simulation {} : The player started with {:10.2f}$".format(i,start_amount))
    print("The player left with {:10.2f}$".format(amount_of_money_left), end='\n\n')

print("Aproximation: ")
print("The player started with {:10.2f}$".format(start_amount))
print("The player left with {:10.2f}$".format(sum(ending_funds)/len(ending_funds)))
print()

plt.show()

"""
    In urma experimentelor, observam ca jucatorul are sanse mai mari de a obtine profit daca plaseaza mai putine pariuri.
    Sansele cresca daca acesta plaseaza pariuri pe numere pare. In unele cazuri, obtinem cifre negative, ceea ce inseamna
    ca jucatorul si-a pierdut toti banii si a acumulat datorii in loc sa obtina profit.
"""