#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from utils import *

N = 1024
L = 10
s = 1
x = np.linspace(-L, L, N)
X, Y = np.meshgrid(x, x)
phi = np.exp(-s*(X**2 + Y**2))

# Laplacian ------------------------------------------------------------

d2phi_expected = (-4*s + 4*s**2*X**2 + 4*s**2*Y**2)*phi

fig, axes = plt.subplots(1, 2)

ax = axes[0]
d2phi = load_array("2dgauss-d2.bin", N)
ax.pcolormesh(X, Y, d2phi.real, cmap="RdBu")
ax.set_aspect("equal")
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.set_title("Laplacian (FFTW)")

ax = axes[1]
ax.pcolormesh(X, Y, d2phi_expected, cmap="RdBu")
ax.set_aspect("equal")
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.set_title("Laplacian (Exact)")

# x derivative ---------------------------------------------------------

dxphi_expected = -2*x*phi

fig, axes = plt.subplots(1, 2)

ax = axes[0]
dxphi = load_array("2dgauss-dx.bin", N)
ax.pcolormesh(X, Y, dxphi.real, cmap="RdBu")
ax.set_aspect("equal")
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.set_title("X derivative (FFTW)")

ax = axes[1]
ax.pcolormesh(X, Y, dxphi_expected, cmap="RdBu")
ax.set_aspect("equal")
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.set_title("X derivative (Exact)")


plt.show()
