#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from utils import *

N = 1024
L = 10
s = 1
q = 2 * np.pi * np.fft.fftfreq(N, d=2 * L / (N - 1))
q = np.fft.fftshift(q)
Qx, Qy = np.meshgrid(q, q)
phi_q_expected = np.pi / s * np.exp(-(Qx**2 + Qy**2) / (4 * s))

phi_q = load_array("2dgauss.bin", N)
# Normalize phi_q (FFTW's output isn't normalized).
phi_q = np.fft.fftshift(phi_q) / (N * N)
# Multiply by 2L twice (for each dimension) to convert the sum into an integral.
phi_q = (2 * L) * (2 * L) * phi_q

fig, axes = plt.subplots(1, 2)

ax = axes[0]

ax.pcolormesh(Qx, Qy, np.abs(phi_q), cmap="RdBu")
ax.set_aspect("equal")
ax.set_title("FFTW")
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)

ax = axes[1]

ax.pcolormesh(Qx, Qy, phi_q_expected, cmap="RdBu")
ax.set_aspect("equal")
ax.set_title("Exact")
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)

plt.show()
