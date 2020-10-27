import numpy as np
import matplotlib.pyplot as pyplot

f = lambda x: (x ** 3) - 7 * (x ** 2) + 14 * x - 6

f_derivat = lambda x: 3 * (x ** 2) - 14 * x + 14


def metoda_newton_raphson(a, b, x0, epsilon):
    x_prev = x0
    x = x0 - f(x0) / f_derivat(x0)

    while (abs(x - x_prev) / abs(x_prev)) >= epsilon:
        x_prev = x
        x = x_prev - f(x_prev) / f_derivat(x_prev)

    return x


a, b = 0., 4. # intervalul initial
epsilon = 1e-5

# Solutia 1
a , b = 0., 1.
x_num1 = metoda_newton_raphson(a, b, 0.5, epsilon)
print('x1: x_num1 = {:.10f}'.format(x_num1))
# Solutia 2
a, b = 1., 3.2
x_num2 = metoda_newton_raphson(a, b, 2.5, epsilon)
print('x2: x_num2 = {:.10f}'.format(x_num2))
# Solutia 3
a, b = 3.2, 4.
x_num3 = metoda_newton_raphson(a, b, 3.5, epsilon)
print('x3: x_num3 = {:.10f}'.format(x_num3))


axis_Ox = np.linspace(0., 4., num=250)
axis_Oy = f(axis_Ox)
x_coordinates = [x_num1, x_num2, x_num3]
y_coordinates = [f(x_num1), f(x_num2), f(x_num3)]


pyplot.figure(0)
pyplot.title('Metoda Newton-Raphson')
pyplot.legend(['f(x)', 'x_num']) 
pyplot.axvline(0, c='black')
pyplot.axhline(0, c='black')
pyplot.xlabel('x') 
pyplot.ylabel('y') 
pyplot.scatter(x_coordinates, y_coordinates, c="red", alpha=1)
pyplot.plot(axis_Ox, axis_Oy, c = "black", linestyle = "-", linewidth = 2)
pyplot.show()