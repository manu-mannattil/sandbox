"""Diffusion equation in 1D using a Chebyshev collocation method."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from utils import *

N = 20
D, x = cheb(N)
dt = 1e-4

A = np.eye(N + 1) - dt*D@D
A[0] = D[0]
A[-1] = D[-1]

# To compute the spatial average of u.
# See Chapter 12 of Trefethen's book.
w = np.linalg.inv(D[1:, 1:])[-1]

xx = np.linspace(-1, 1, 100)
u = np.exp(-3*x*x)

fig, ax = plt.subplots()
ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$u(x)$")
ax.set_ylim(-1.5, 1.5)
uu = np.polyval(np.polyfit(x, u, N), xx)
line, = ax.plot(xx, uu)

def animate(i):
    global u
    b = u.copy()
    b[0] = 0
    b[-1] = 0
    u = np.linalg.solve(A, b)
    uu = np.polyval(np.polyfit(x, u, N), xx)
    line.set_ydata(uu)
    print("average u = ", w.dot(u[1:]))
    return line,

ani = FuncAnimation(fig, animate, frames=100, interval=1, blit=True)
plt.show()
