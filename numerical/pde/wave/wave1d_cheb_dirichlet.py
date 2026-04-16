# -*- coding: utf-8 -*-

"""Solves the 1D wave equation using Chebyshev collocation.

    u_tt = u_xx     u in [-1, 1]
    u = 0           x = -1, x = 1 (Dirichlet BC)

In case of a string, the BC corresponds to tied ends.  So there's
a phase change when the wave gets reflected back.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import warnings
warnings.filterwarnings("ignore", category=np.exceptions.RankWarning)

def cheb(N):
    """Compute the Chebyshev differentiation matrix and nodes."""
    k = np.arange(N + 1)

    # Chebyshev nodes
    x = -np.cos(np.pi * k / N)
    if N % 2 == 0:
        x[N // 2] = 0.0  # enforce exact zero for symmetry

    # Coefficients with alternating signs
    c = np.ones(N + 1)
    c[[0, -1]] = 2
    c *= (-1) ** k
    c = c[:, None]  # column vector

    # Pairwise differences matrix
    X = np.tile(x[:, None], (1, N + 1))
    dX = X - X.T

    # Differentiation matrix (off-diagonal entries)
    D = (c @ (1 / c).T) / (dX + np.eye(N + 1))

    # Set diagonal entries so each row sums to zero
    D -= np.diag(D.sum(axis=1))

    return D, x

N = 50
D, x = cheb(N)
D2 = D@D

# Time step.
dt = 1e-3

# Initial perturbation is a Gaussian.
xx = np.linspace(-1, 1, 1000)
u = np.exp(-100*x*x)
# In the past, let's put the wave to the right of the origin.
# So, this is a leftward moving wave.
u_old = np.exp(-100*(x - dt)*(x - dt))

fig, ax = plt.subplots()
ax.set_title("1d wave equation using Chebyshev differentiation")
ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$u(x)$")
ax.set_ylim(-1.5, 1.5)

xx = np.linspace(-1, 1, 1000)
line, = ax.plot(xx, np.polyval(np.polyfit(x, u, N), xx))

def animate(i):
    global u, u_old

    # Use Chebyshev differentiation to find u_xx.
    u_xx = D2@u

    # Leapfrog integration in real space.
    u_new = 2*u - u_old + dt**2*u_xx
    u_old = u
    u = u_new

    # Boundary conditions.
    u[0] = 0
    u[-1] = 0

    line.set_ydata(np.polyval(np.polyfit(x, u, N), xx))
    return line,

ani = FuncAnimation(fig, animate, frames=1, interval=1, blit=True)
plt.show()
