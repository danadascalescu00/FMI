from sys import exit
import numpy as np

# A = np.array([[2., -1., -2.], [4., 2., 0.], [0., -2., -1.]])
A = np.array([[1., 2., 3.], [4., 5., 6.], [7., 8., 10.]])
b = np.array([[4., 4., 7.]]).T
n = A.shape[0]

# Pasul 1: Verificam daca sistemul are solutii(determinantul matricei trebuie sa fie diferit de 0)
if abs(np.linalg.det(A)) < 1e-5:
    print("Determinantul matricei este null, prin urmare sistemul nu are solutii!")
    exit(1)

U = np.copy(A) # matricea superior triunghiulara
L = np.zeros(A.shape) # matricea inferior triunghiulara
P = np.identity(n)

""" 
    Gauss cu pivotare partiala
"""
for k in range(0, n-1):
    p = np.argmax(np.abs(U[k:,k]))
    # interschimbam liniile p si k in U, P, L
    U[[p,k]] = U[[k,p]]
    P[[p,k]] = P[[k,p]] 
    L[[p,k]] = L[[k,p]]
    for i in range(k + 1, n):
        L[i][k] = U[i][k] / U[k][k]
        U[i] = U[i] - (L[i][k] * U[k])
L += np.identity(n)

print('U: \n', U)
print('L: \n', L)
print('\n P @ A == L @ U:')
print( P @ A == L @ U, '\n')


# Metoda Substitutiei Ascendente
def metoda_substitutiei_ascendente(L, C):
    y = np.zeros(n)
    for i in range(0, n):
        y[i] = (C[i] - np.dot(L[i,:i+1], y[:i+1])) / L[i,i]
    return y


# Metoda Substitutiei Descendente
def metoda_substitutiei_descendente(U, C):
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = (C[i] - np.dot(U[i,i+1:], x[i+1:])) / U[i][i]
    return x


if __name__ == "__main__":
    b = P @ b
    y = metoda_substitutiei_ascendente(L, b)
    x = metoda_substitutiei_descendente(U, y)
    print('x = ', x)
    print('A @ x', A@x)