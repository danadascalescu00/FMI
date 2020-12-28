import numpy as np
import matplotlib.pyplot as plt

# Domeniul functiei
# left, right = -np.pi, np.pi
left, right = -1, 1

# Functia pe care dorim sa o aproximam
def fun(x):
    return np.cos(2*x) - 2 * np.sin(3*x)

def fun2(x):
    return 1 / (1 + 25 * (x  ** 2))


# definim gradul polinomului de interpolare
n = 36

# Daca este setat la False se foloseste o discretizare echidistanta
# Daca este setat la False se foloseste o discretizare echidistanta
n_cebasev =  True

def nod_cebasev(a,b,k,n):
    return .5 * (a + b) + .5 * (b - a) * np.cos(((2 * k - 1) / (2 * n)) * np.pi )

def noduri_cebasev(a,b,n):
    return np.array([nod_cebasev(a,b,k,n) for k in range(1,n+1)])


def plot_function(x_grafic, y_grafic):
    plt.figure(0)
    plt.title('Functia f')
    plt.legend(['f(x)', 'x']) 
    plt.axvline(0, c='black')
    plt.axhline(0, c='black')
    plt.xlabel('x') 
    plt.ylabel('y') 
    plt.plot(x_grafic, y_grafic, c="black", linestyle="-", linewidth=2)


def eval_polinom(a,x):
    sum = 0
    for i in range(n+1):
        sum += a[i] * (x ** i)
    return sum


def polinom(a, points):
    return np.array([eval_polinom(a, x) for x in points])


def L(k, x, x_coordinates):
    prod = 1
    for j in range(n+1):
        if j != k:
            prod = prod *  (x - x_coordinates[j]) / (x_coordinates[k] - x_coordinates[j])
    return prod


def polinom_Lagrange(x, x_coordinates, y_coordinates):
    sum = 0
    for j in range(n+1):
        sum += L(j, x, x_coordinates) * y_coordinates[j]

    return sum


if __name__ == "__main__":

    x_grafic = np.linspace(left, right, 100)            
    y_grafic = fun2(x_grafic)

    # Obtinem nodurile de interpolare
    x_coordinates = None
    if n_cebasev:
        x_coordinates = noduri_cebasev(left,right,n+1)
    else:
        x_coordinates = np.linspace(left,right,n+1)
    y_coordinates = fun2(x_coordinates)

    # Plotam functia
    plot_function(x_grafic, y_grafic)
    # plotam nodurile de interpolare
    plt.scatter(x_coordinates, y_coordinates, c="blue", alpha=1)

    # Prima metoda de interpolare - metoda directa
    # Determinam coeficientii polinomului de interpolare rezolvand sistemul V*a=y
    V = np.vander(x_coordinates, N=n+1, increasing=True) # matricea Vandermonde pentru sistemul pe care urmeaza sa-l rezolvam
    # rezolvam sistemul V * a = y
    a1 = np.linalg.solve(V, y_coordinates)

    plt.plot(x_grafic, polinom(a1,x_grafic), linestyle='--', color = 'red')
    plt.show()

    # A doua metoda de interpolare - polinomul Lagrange
    y_lagrange = np.zeros(x_grafic.shape)
    for i in range(y_lagrange.shape[0]):
        y_lagrange[i] = polinom_Lagrange(x_grafic[i], x_coordinates, y_coordinates) 

    # Plotam functia
    plot_function(x_grafic, y_grafic)
    # plotam nodurile de interpolare
    plt.scatter(x_coordinates, y_coordinates, c="blue", alpha=1)
    plt.plot(x_grafic, y_lagrange, linestyle= '--', color='red')
    plt.show()

    # Eroarea absoluta si relativa
    abs_error1 = np.abs(polinom(a1,x_grafic) - fun2(x_grafic))
    abs_error2 = np.abs(y_lagrange - fun2(x_grafic))
    rel_error1 = abs_error1 / max(fun2(x_grafic))
    rel_error2 = abs_error2 / max(fun2(x_grafic))


    fig, (ax1, ax2) = plt.subplots(2)
    fig.suptitle('Eroarea de trunchiere - Metoda directa / Lagrange')
    ax1.plot(x_grafic, rel_error1)
    ax2.plot(x_grafic, rel_error2)
    plt.show()