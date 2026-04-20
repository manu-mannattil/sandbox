# -*- coding: utf-8 -*-

"""Solves the 2D wave equation using Chebyshev collocation.

    u_tt = u_xx + u_yy      (x, y) in [-1, 1] x [-1, 1]
    u = 0                   x = -1, x = 1, y = -1, y = 1 (Dirichlet BC)

There's a phase change when the wave gets reflected back.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def cheb(N):
    """Compute the Chebyshev collocation matrix and nodes."""
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

def rescale(u, interval=(-1, 1)):
    # Rescale the values of the given field into a desired interval.
    u = np.asarray(u)
    return (interval[0] + (u - np.min(u)) * (interval[1] - interval[0]) / (np.max(u) - np.min(u)))

N = 100
D, x = cheb(N)
D2 = D@D
X, Y = np.meshgrid(x, x)

# Time step.
dt = 1e-4

# Initial perturbation is a Gaussian.
u = np.exp(-100*(X*X + Y*Y))
u_old = u

fig, ax = plt.subplots()
ax.set_title("2D wave equation (Dirichlet BC)")
ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$u(x)$")
ax.set_ylim(-1, 1)

xx = np.linspace(-1, 1, 1000)
im = ax.pcolormesh(X, Y, rescale(u), cmap="RdBu_r")
ax.set_aspect("equal")

def animate(i):
    global u, u_old

    # Use Chebyshev collocation to find Laplacian(u).
    # D2@u is u_xx and u@D2.T is u_yy.
    Lu = D2@u + u@D2.T

    # Leapfrog integration in real space.
    u_new = 2*u - u_old + dt**2*Lu
    u_old = u
    u = u_new

    # Boundary conditions.
    u[0] = np.zeros(N + 1)
    u[-1] = np.zeros(N + 1)
    u[:, 0] = np.zeros(N + 1)
    u[:, -1] = np.zeros(N + 1)

    im.set_array(rescale(u))
    return im,

ani = FuncAnimation(fig, animate, frames=1, interval=1, blit=True)
plt.show()
