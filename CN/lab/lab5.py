from sys import exit
import numpy as np

# exemplul 1
A = np.array([[1., 2., 3.], [4., 5., 6.], [7., 8., 10.]])
C = np.array([[4., 4., 7.]]).T

# exemplul 2
# epsilon = pow(10,16)
# A = np.array([[1. , epsilon], [1. , 1.]])
# C = np.array([[epsilon, 2.]]).T

n = A.shape[0]
x = np.zeros(n)

# Pasul 1: Verificam daca sistemul are solutii(determinantul matricei trebuie sa fie diferit de 0)
if abs(np.linalg.det(A)) < 1e-5:
    print("Determinantul matricei este null, prin urmare sistemul nu are solutii!")
    exit(1)

# Pasul 2: Aplicam metoda Gauss cu pivotare totala
indices = np.arange(0, n)
A_extins = np.concatenate((A, C), axis = 1)

for k in range(0, n - 1):
    submatrice = A_extins[k:, k:n-1]
    (p, m) = np.unravel_index(submatrice.argmax(), submatrice.shape)
    p, m = p + k, m + k
    
    # Daca p != k atunci interschimbam liniile p si k, iar daca m != k interschimbam coloanele m si k
    A_extins[[p,k]] = A_extins[[k,p]]
    A_extins[:, [k, m]] = A_extins[:, [m, k]]
    # Schimbam indicii necunoscutelor
    indices[m], indices[k] = indices[k], indices[m]

    for l in range(k + 1, n):
        A_extins[l] = A_extins[l] - (A_extins[l][k] / A_extins[k][k]) * A_extins[k]


U = np.copy(A_extins[0:n])
U = np.delete(U, n, axis = 1)
C = A_extins[:,n]


""" 
    Pasul 3: Mergem de la ultima linie catre prima, rezolvand sistemul prin substitutie 
             (Metoda substitutiei descendente)
"""
for i in range(n-1, -1, -1):
    x[i] = (C[i] - np.dot(U[i,i+1:], x[i+1:])) / U[i][i]

# La interschimbarea a doua coloane se schimba ordinea necunoscutelor in vectorul x
print('x = ', x[indices])
print('A @ x = ', A @ x[indices])


# Aplicatii ale metodei Gauss --- Calcularea determinantului unei matrice
print('\nAplicatii ale metodei Gauss:\nCalcularea determinantului unei matrice')
A = np.array([[2., -1., -2.], [4. , 2., 0.], [0., -2., -1.]])
I = np.array([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]]).T

n = A.shape[0]
x = np.zeros(A.shape)

# Aplicam metoda Gauss cu pivotare totala
indices = np.arange(0, n)
A_extins = np.concatenate((A, I), axis = 1)
s = 0 # numarul de schimbari de linii

for k in range(0, n - 1):
    submatrice = A_extins[k:, k:n-1]
    (p, m) = np.unravel_index(submatrice.argmax(), submatrice.shape)
    p, m = p + k, m + k
    
    if p != k:
        s += 1
    
    if m != k:
        s += 1

    # Daca p != k atunci interschimbam liniile p si k, iar daca m != k interschimbam coloanele m si k
    A_extins[[p,k]] = A_extins[[k,p]]
    A_extins[:, [k, m]] = A_extins[:, [m, k]]
    # Schimbam indicii necunoscutelor
    indices[m], indices[k] = indices[k], indices[m]

    for l in range(k + 1, n):
        A_extins[l] = A_extins[l] - (A_extins[l][k] / A_extins[k][k]) * A_extins[k]


U = np.copy(A_extins[0:n])

determinant = 1.
for i in range(n):
    determinant *= U[i][i]

"""
    Daca intr-o matrice patratica se schimba intre ele doua linii(sau coloane) se obtine o matrice care are
    determinantul egal cu opusul determinantului matricei initiale
"""
determinant = (-1)**s * determinant
print('Determinantul matricei obtinut folosind Gauss cu pivotare totala: ', determinant)
print('Determinantul matricei folosind np.linalg.det: ', np.linalg.det(A))