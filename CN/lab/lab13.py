import numpy as np
import matplotlib.pyplot as plt

n = 50 # numarul de puncte ales pentru discretizarea intervalului [a,b]
metoda_aproximare = 'progresiva' #'progresiva'/'regresiva'/'centrala'

# Domeniul functiei - intervalul [a,b]
left, right = -np.pi, np.pi

# Functia pe care dorim sa o aproximam
def f(x):
    return np.sin(x)

def f_derivat(x):
    return np.cos(x)

# discretizam intervalul [a,b]
x_grafic = np.linspace(left, right, n+1)
y_grafic = f(x_grafic)
h = x_grafic[1] - x_grafic[0]

# aproximam numeric f_derivat
f_derivat_progresiv = np.zeros(x_grafic.shape[0])
f_derivat_regresiv = np.zeros(x_grafic.shape[0])
f_derivat_central = np.zeros(x_grafic.shape[0])
for i in range(1,n):
    f_derivat_progresiv[i] = (y_grafic[i+1] - y_grafic[i]) / h
    f_derivat_regresiv[i] = (y_grafic[i] - y_grafic[i-1]) / h
    f_derivat_central[i] = (y_grafic[i+1] - y_grafic[i-1]) / (2*h)

fig, (ax1, ax2, ax3) = plt.subplots(3)
fig.suptitle('Progresiva/Regresiva/Centrala')
ax1.plot(x_grafic[1:n], f_derivat_progresiv[1:n])
ax1.plot(x_grafic[1:n], f_derivat(x_grafic[1:n]), linestyle= '--', color='red')
ax2.plot(x_grafic[1:n], f_derivat_regresiv[1:n])
ax2.plot(x_grafic[1:n], f_derivat(x_grafic[1:n]), linestyle= '--', color='red')
ax3.plot(x_grafic[1:n], f_derivat_central[1:n])
ax3.plot(x_grafic[1:n], f_derivat(x_grafic[1:n]), linestyle= '--', color='red')
plt.show()

# Eroarea absoluta si relativa
abs_error1 = np.abs(f_derivat_progresiv[1:n] - f_derivat(x_grafic[1:n]))
abs_error2 = np.abs(f_derivat_regresiv[1:n] - f_derivat(x_grafic[1:n]))
abs_error3 = np.abs(f_derivat_central[1:n] - f_derivat(x_grafic[1:n]))

rel_error1 = abs_error1 / max(f_derivat(x_grafic[1:n]))
rel_error2 = abs_error2 / max(f_derivat(x_grafic[1:n]))
rel_error3 = abs_error3 / max(f_derivat(x_grafic[1:n]))


fig, (ax1, ax2, ax3) = plt.subplots(3)
fig.suptitle('Eroarea absoluta/relativa')
ax1.plot(x_grafic[1:n], rel_error1)
ax2.plot(x_grafic[1:n], rel_error2)
ax3.plot(x_grafic[1:n], rel_error3)
plt.show()