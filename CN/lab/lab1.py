
import numpy as np
from math import floor, log2
import matplotlib.pyplot as pyplot

# Definim functia pentru care vrem sa gasim solutia
def f(x):
    fct = (x ** 3) - 7 * (x ** 2) + 14 * x - 6
    return fct

def metoda_bisectiei(a, b, epsilon):
    assert f(a)*f(b) < 0, "E posibil sa nu existe solutie"

    x_num = (a + b) / 2
    num_iterations = floor(log2((b - a)/ epsilon) - 1)

    for i in range(1, num_iterations):
        if f(x_num) == 0:
            break
        elif f(a) * f(x_num) < 0:
            b = x_num
        else:
            a = x_num
        x_num = (a + b) / 2

    return x_num



def main():
    epsilon = 1e-5

    # Solutia 1
    a , b = 0., 1.
    x_num1 = metoda_bisectiei(a, b, epsilon)
    print('x1: ', x_num1)
    # Solutia 2
    a, b = 1., 3.2
    x_num2 = metoda_bisectiei(a, b, epsilon)
    print('x2: ', x_num2)
    # Solutia 3
    a, b = 3.2, 4.
    x_num3 = metoda_bisectiei(a, b, epsilon)
    print('x3: ', x_num3)

    
    axis_Ox = np.linspace(0., 4., num=200)
    axis_Oy = f(axis_Ox)
    x_coordinates = [x_num1, x_num2, x_num3]
    y_coordinates = [f(x_num1), f(x_num2), f(x_num3)]

    pyplot.figure(0)
    pyplot.title('Metoda bisectiei')
    pyplot.legend(['f(x)', 'x_num']) 
    pyplot.axvline(0, c='black')
    pyplot.axhline(0, c='black')
    pyplot.xlabel('x') 
    pyplot.ylabel('y') 
    pyplot.scatter(x_coordinates, y_coordinates, c="red", alpha=1)
    pyplot.plot(axis_Ox, axis_Oy, c = "black", linestyle = "-", linewidth = 2)
    pyplot.show()




if __name__ == "__main__":
    # Sa se gaseasca cele trei solutii ale ecuatii urmatoare: x^3 -7x^2 + 4x - 6 = 0 pe intervalul [0,4] cu o precizie Epsilon = 10^(-5)
    # HINT: Se vor alege intervalele [0,1], [1,3.2] si [3.2,4].
    main()
