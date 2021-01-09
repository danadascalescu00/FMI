import sys
import numpy as np
import pdb


def select_random_path(E):
    # pentru linia 0 alegem primul pixel in mod aleator
    line = 0
    col = np.random.randint(low=0, high=E.shape[1], size=1)[0]
    path = [(line, col)]
    for i in range(1, E.shape[0]):
        # alege urmatorul pixel pe baza vecinilor
        line = i
        # coloana depinde de coloana pixelului anterior
        if path[-1][1] == 0:  # pixelul este localizat la marginea din stanga
            opt = np.random.randint(low=0, high=2, size=1)[0]
        elif path[-1][1] == E.shape[1] - 1:  # pixelul este la marginea din dreapta
            opt = np.random.randint(low=-1, high=1, size=1)[0]
        else:
            opt = np.random.randint(low=-1, high=2, size=1)[0]
        col = path[-1][1] + opt
        path.append((line, col))

    return path


def select_greedy_path(E):
    # pentru linia 0 se alege pixelul de pe coloana care are valoarea minima
    line = 0
    col = np.argmin(E[line,:])
    path = [(line, col)]
    # la fiecare pas se alege cea mai buna solutie locala (pixelii cu gradientul cel mai mic)
    for i in range(1,E.shape[0]):
        # alege urmatorul pixel pe baza vecinilor
        line = i 
        # coloana depinde de coloana pixelului anterior
        prev_col = path[-1][1]
        if prev_col == 0:  # pixelul este localizat la marginea din stanga
            opt = np.argmin(E[line, prev_col:prev_col+2])
        elif prev_col == E.shape[1] - 1:  # pixelul este localizat la marginea din dreapta
            opt = np.argmin(E[line, prev_col-1:prev_col+1]) - 1
        else:
            opt = np.argmin(E[line, prev_col-1:prev_col+2]) - 1
        col = prev_col + opt
        path.append((line, col))            

    return path


def select_dynamic_programming_path(E):
    n = E.shape[0]
    # matricea de drumuri ce retine pentru fiecare pixel (i,j) drumul de cost minim pana la acesta
    # costul unui drum este suma magnitudinilor gradientilor pixelilor ce alcatuiesc drumul
    M = np.zeros(E.shape, dtype=np.float64) 
    M[0,:] = E[0,:]
    for i in range(1,n):
        for j in range(E.shape[1]):
            if j == 0: # pixelul este localizat la marginea din stanga
                M[i,j] = E[i,j] + np.amin(M[i-1,j:j+2])
            elif j == E.shape[1] - 1: # pixelul este localizat la marginea din dreapta
                M[i,j] = E[i,j] + np.amin(M[i-1,j-1:j+1])
            else:
                M[i,j] = E[i,j] + np.amin(M[i-1,j-1:j+2])

    # drumul vertical format din n pixeli
    path = [(-1,-1)] * n 
    # valoarea minima din ultima linie a matricei de drumuri M reprezinta valoarea drumului optim, iar
    # pozitia valorii minime localizeaza ultimul pixel din insiruire
    line, col = n - 1, np.argmin(M[n-1,:])
    path[line] = (line,col)
    # gasim drumul de cost minim mergand inapoi si gasind drumul cu ajutorul celor 3 vecini de sus din M
    for i in range(n-2, -1, -1):
        # alege urmatorul pixel pe baza vecinilor
        line = i
        prev_col = path[i+1][1]
        if prev_col == 0: # pixelul este localizat la marginea din stanga
            opt = np.argmin(M[i,prev_col:prev_col+2])
        elif prev_col == M.shape[1] - 1: # pixelul este localizat la marginea din dreapta
            opt = np.argmin(M[i,prev_col-1:prev_col+1]) - 1
        else:
            opt = np.argmin(M[i,prev_col-1:prev_col+2]) - 1
        col = prev_col + opt
        path[i] = (line,col)

    return path


def select_path(E, method):
    if method == 'aleator':
        return select_random_path(E)
    elif method == 'greedy':
        return select_greedy_path(E)
    elif method == 'programareDinamica':
        return select_dynamic_programming_path(E)
    else:
        print('The selected method %s is invalid.' % method)
        sys.exit(-1)