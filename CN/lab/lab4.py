from sys import exit
import numpy as np

# A = np.array([[2., -1., -2.], [4., 2., 0.], [0., -2., -1.]])
# C = np.array([[-1., 6., -3.]]).T

# Limitarile metodei
epsilon = 1e-20
A = np.array([[epsilon, 1.], [1., 1.]])
C = np.array([[1. , 2.]]).T

n = A.shape[0]
x = np.zeros(n)

# Pasul 1: Verificam daca sistemul are solutii(determinantul matricei trebuie sa fie diferit de 0)
if abs(np.linalg.det(A)) < 1e-5:
    print("Determinantul matricei este null, prin urmare sistemul nu are solutii!")
    exit(1)


# Pasul 2: Aplicam Metoda Gauss cu pivotare partiala
A_extins = np.concatenate((A, C), axis = 1)

for k in range(0, n-1):
    p = np.argmax(np.abs(A[k:][k])) + k
    A_extins[[p,k]] = A_extins[[k,p]] 
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

print('x = ', x)
print('U @ x = ', U @ x)