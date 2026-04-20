"""Diffusion equation in 1D with a variable mobility.

    u_t = (Mu_x)_x

Add and subtract alpha*u_xx:

    u_t - alpha*u_xx = (Mu_x)_x + alpha*u_xx

Evaluate the RHS terms explicitly.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from utils import *

N = 20
D, x = cheb(N)
dt = 1e-4

def M(u):
    """Diffusivity."""
    return 0.5*(1 + np.tanh(u))

alpha = 2

C = 0.1
A = np.eye(N + 1) - dt*alpha*D@D
A[0] = D[0]
A[-1] = D[-1]

# To compute the spatial average of u.
# See Chapter 12 of Trefethen's book.
w = np.linalg.inv(D[1:, 1:])[-1]

xx = np.linspace(-1, 1, 100)
u = np.tanh(-3*x)

fig, ax = plt.subplots()
ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$u(x)$")
ax.set_ylim(-1.5, 1.5)
uu = np.polyval(np.polyfit(x, u, N), xx)
line, = ax.plot(xx, uu)

def animate(i):
    global u
    rhs = dt*D@(M(u)*(D@u) - alpha*D@u) + u + C*dt

    # Enforce BC.
    rhs[0] = 0
    rhs[-1] = 0

    u = np.linalg.solve(A, rhs)
    uu = np.polyval(np.polyfit(x, u, N), xx)
    line.set_ydata(uu)
    print("average u = ", w.dot(u[1:]))
    return line,

ani = FuncAnimation(fig, animate, frames=100, interval=1, blit=True)
plt.show()
