import numpy as np
import matplotlib.pyplot as plt

# Domeniul functiei
left, right = -np.pi, np.pi
print(left, right)

# Functia pe care dorim sa o aproximam
def fun(x):
    return np.cos(2*x) - 2 * np.sin(3*x)


# definim gradul polinomului de interpolare
n = 25


def eval_polinom(a,x):
    sum = 0
    for i in range(n+1):
        sum += a[i] * (x ** i)
    return sum


def polinom(a, points):
    return np.array([eval_polinom(a, x) for x in points])


if __name__ == "__main__":
    x_grafic = np.linspace(left, right, 100)
    y_grafic = fun(x_grafic)

    # Obtinem nodurile de interpolare
    x_coordinates = np.linspace(left, right, n+1)
    y_coordinates = fun(x_coordinates)

    # Plotam functia
    plt.figure(0)
    plt.title('Functia f')
    plt.legend(['f(x)', 'x']) 
    plt.axvline(0, c='black')
    plt.axhline(0, c='black')
    plt.xlabel('x') 
    plt.ylabel('y') 
    plt.plot(x_grafic, y_grafic, c="black", linestyle="-", linewidth=2)
    # plotam nodurile de interpolare
    plt.scatter(x_coordinates, y_coordinates, c="blue", alpha=1)

    # Determinam coeficientii polinomului de interpolare rezolvand sistemul V*a=y
    V = np.vander(x_coordinates, N=n+1, increasing=True) # matricea Vandermonde pentru sistemul pe care urmeaza sa-l rezolvam
    # rezolvam sistemul V * a = y
    a = np.linalg.solve(V, y_coordinates)

    plt.plot(x_grafic, polinom(a,x_grafic), linestyle='--', color = 'red')
    plt.show()

    # Eroarea absoluta si relativa
    abs_error = np.abs(polinom(a,x_grafic) - fun(x_grafic))
    rel_error = abs_error / max(fun(x_grafic))

    fig, (ax1, ax2) = plt.subplots(2)
    fig.suptitle('Eroarea absoluta/relativa')
    ax1.plot(x_grafic, abs_error)
    ax2.plot(x_grafic, rel_error)
    plt.show()