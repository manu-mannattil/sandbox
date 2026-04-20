#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fftshift, fft2, ifft2

N = 1024
x = np.linspace(-10, 10, N)
X, Y = np.meshgrid(x, x)
dx = x[1] - x[0]

a = 3
b = 4

# In FFT convention, the origin is not in the middle, but is at the corners.
# So do an FFT shift to make sure that the "origins" align.
f = np.exp(-a*(X**2 + Y**2))
f = np.fft.fftshift(f)

g = np.exp(-b*(X**2 + Y**2))

fq = fft2(f)
gq = fft2(g)

# XXX: Why is a multiplication with dx^2 necessary?
fgq = fq*gq*dx*dx
fg = ifft2(fgq).real

fig, axes = plt.subplots(1, 2)

ax = axes[0]

# Expected result.
fg_exp = np.exp(-a*b/(a+b)*(X**2+Y**2))*np.pi/(a+b)
ax.pcolormesh(X, Y, fg_exp)
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect("equal")

# Fourier.
ax = axes[1]
ax.pcolormesh(X, Y, fg)
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect("equal")

plt.show()
