import numpy as np
import matplotlib.pyplot as plt

# Domeniul functiei
left, right = 2, 4

# numarul de intervale
n = 2

# Functia pe care dorim sa o aproximam
def fun(x):
    return (x-3)**2 + 2

def fun_derivat(x):
    return 2*(x-3)

def plot_function(x_grafic, y_grafic):
    plt.figure(0)
    plt.title('Functia f')
    plt.legend(['f(x)', 'x']) 
    plt.axvline(0, c='black')
    plt.axhline(0, c='black')
    plt.xlabel('x') 
    plt.ylabel('y') 
    plt.plot(x_grafic, y_grafic, c="black", linestyle="-", linewidth=2)


x_grafic = np.linspace(left, right, 100)            
y_grafic = fun(x_grafic)

# Obtinem nodurile de interpolare
x_coordinates = np.linspace(left, right, n+1)
y_coordinates = fun(x_coordinates)

# Plotam functia
plot_function(x_grafic, y_grafic)
# plotam nodurile de interpolare
plt.scatter(x_coordinates, y_coordinates, c="blue", alpha=1)


def spline_patratica(a,b,c,x_i):
    return lambda x : a + b * (x - x_i) + c * (x - x_i) ** 2

a = y_coordinates
b = np.zeros(a.shape[0])
b[0] = fun_derivat(x_coordinates[0])
for i in range(n-1):
    h = (x_coordinates[i+1] - x_coordinates[i])
    b[i+1] = 2 * (y_coordinates[i+1] - y_coordinates[i]) / h - b[i]

c = np.zeros(a.shape[0])
for i in range(n):
    h = (x_coordinates[i+1] - x_coordinates[i])
    c[i] = (y_coordinates[i+1] - y_coordinates[i] - b[i] * h) / (h ** 2)

S = np.piecewise(
        x_grafic,
        [
            (x_coordinates[i] <= x_grafic) & (x_coordinates[i+1] > x_grafic) for i in range(n-1)
        ],
        [
            spline_patratica(a[i],b[i],c[i],x_coordinates[i]) for i in range(n)
        ] 
    )

plt.plot(x_grafic, S, linestyle= '--', color='red')
plt.show()

# Eroarea absoluta si relativa
abs_error = np.abs(S - fun(x_grafic))
rel_error = abs_error / max(fun(x_grafic))

fig, (ax1, ax2) = plt.subplots(2)
fig.suptitle('Eroarea absoluta/relativa')
ax1.plot(x_grafic, abs_error)
ax2.plot(x_grafic, rel_error)
plt.show()