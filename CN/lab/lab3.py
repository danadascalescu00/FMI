from sys import exit
import numpy as np

U = np.array([[2., -1., -2.], [0., 4., 4.], [0., 0., 1.]])
C = np.array([[-1., 8., 1.]]).T

n = U.shape[0]
x = np.zeros(n)

# Pasul 1: Verificam daca sistemul are solutii(determinantul matricei trebuie sa fie diferit de 0)
if abs(np.linalg.det(U)) < 1e-5:
    print("Determinantul matricei este null, prin urmare sistemul nu are solutii!")
    exit(1)

# Pasul 2: Mergem de la ultima linie catre prima, rezolvand sistemul prin substitutie (Metoda substitutiei descendente)
for i in range(n-1, -1, -1):
    x[i] = (C[i] - np.dot(U[i,i+1:], x[i+1:])) / U[i][i]

print('x = ', x)
print('U @ x = ', U @ x)
