from sys import exit
import numpy as np

# exxemplul 1
# A = np.array([[1., 2., 3.], [4., 5., 6.], [7., 8., 10.]])
# C = np.array([[4., 4., 7.]]).T

# exemplul 2
epsilon = pow(10,16)
A = np.array([[1. , epsilon], [1. , 1.]])
C = np.array([[epsilon, 2.]]).T

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
    submatrice = A_extins[k:, k:n]
    (p, m) = np.unravel_index(submatrice.argmax(), submatrice.shape)
    p, m = p + k, m + k

    if A_extins[p][m] == 0:
        print('Sistemul este incompatibil sau compatibil nedeterminat!')
        exit(1)
    
    A_extins[[p,k]] = A_extins[[k,p]]
    A_extins[:, [k, m]] = A_extins[:, [m, k]]
    indices[m], indices[k] = indices[k], indices[m]

    for l in range(k + 1, n):
        A_extins[l] = A_extins[l] - (A_extins[l][k] / A_extins[k][k]) * A_extins[k]


if A_extins[n - 1][n - 1] == 0:
    print('Sistemul este incompatibil sau compatibil nedeterminat!')
    exit(1)


U = np.copy(A_extins[0:n])
U = np.delete(U, n, axis = 1)
C = A_extins[:,n]

""" 
    Pasul 3: Mergem de la ultima linie catre prima, rezolvand sistemul prin substitutie 
             (Metoda substitutiei descendente)
"""
for i in range(n-1, -1, -1):
    x[i] = (C[i] - np.dot(U[i,i+1:], x[i+1:])) / U[i][i]

print('x = ', x[indices])
print('A @ x = ', A @ x[indices])