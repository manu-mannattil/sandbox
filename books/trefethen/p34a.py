"""Allen-Cahn equation with Neumann BC du/dx(1) = du/dx(-1) = 0."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from utils import *

N = 20
D, x = cheb(N)
D2 = D@D

# At each time step, we adjust u(-1) and u(1) to ensure that the Neumann
# BCs are obeyed.
B = np.array([D[0][1:-1], D[-1][1:-1]])
A = np.array([[D[0][0], D[0][-1]],
              [D[-1][0], D[-1][-1]]])
BC = -np.linalg.inv(A)@B

eps = 0.01
dt = 0.01

u = x**3
xx = np.linspace(-1, 1, 100)

fig, ax = plt.subplots()
ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$u(x)$")
ax.set_ylim(-1.5, 1.5)
uu = np.polyval(np.polyfit(x, u, N), xx)
line, = ax.plot(xx, uu)

def animate(i):
    global u
    u += dt*(eps*D2@u + u - u**3)
    u[0], u[-1] = BC@u[1:-1]

    uu = np.polyval(np.polyfit(x, u, N), xx)
    line.set_ydata(uu)
    return line,

ani = FuncAnimation(fig, animate, frames=100, interval=1, blit=True)
plt.show()
