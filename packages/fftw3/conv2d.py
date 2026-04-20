#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from utils import *

n = 1024
L = 10
x = np.linspace(-L, L, n)
X, Y = np.meshgrid(x, x)

K_phi = load_array("conv2d.bin")

fig, axes = plt.subplots(1, 2)

ax = axes[0]

ax.pcolormesh(X, Y, K_phi.real, cmap="RdBu")
ax.set_aspect("equal")
ax.set_title("FFTW")
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)

ax = axes[1]

# Compare with exact.
alpha, beta = 1.0, 0.5
a, b = -4.0, 3.0
gamma = alpha*beta/(alpha+beta)
delta = a + b
K_phi_exact = np.pi*gamma/(alpha*beta)*np.exp(-gamma*((X-delta)**2 + (Y-delta)**2))

ax.pcolormesh(X, Y, K_phi_exact, cmap="RdBu")
ax.set_aspect("equal")
ax.set_title("Exact")
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)

plt.show()
