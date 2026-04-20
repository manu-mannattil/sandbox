# -*- coding: utf-8 -*-

"""Computes the Laplacian of a 2D Gaussian exp(-s*(x**2+y**2))."""

import numpy as np
from scipy.fft import fftn, ifftn, fftfreq
import matplotlib.pyplot as plt

# Make data ------------------------------------------------------------

N = 2**10
x = np.linspace(-10, 10, N)
dx = x[1] - x[0]

# Gaussian
X, Y = np.meshgrid(x, x)
s = 0.2
f = np.exp(-s*(X**2 + Y**2))

# Fourier transform of Gaussian.
fq = fftn(f)
q = fftfreq(N, d=dx/(2*np.pi))
q2 = q[:, None]**2 + q[None, :]**2

# Laplacian ------------------------------------------------------------

dfq = -q2*fq
df = ifftn(dfq).real

fig, axes = plt.subplots(1, 2)

ax = axes[0]

# Expected result.
df_exp = (-4*s + 4*s**2*X**2 + 4*s**2*Y**2)*f
ax.set_title("Expected")
ax.pcolormesh(X, Y, df_exp)
ax.set_aspect("equal")

# Fourier.
ax = axes[1]
ax.pcolormesh(X, Y, df)
ax.set_title("FFT")
ax.set_aspect("equal")

# x derivative ---------------------------------------------------------

dfq = 1j*q*fq
df = ifftn(dfq).real

fig, axes = plt.subplots(1, 2)

ax = axes[0]

# Expected result.
df_exp = (-2*x*s)*f
ax.set_title("Expected")
ax.pcolormesh(X, Y, df_exp)
ax.set_aspect("equal")

# Fourier.
ax = axes[1]
ax.pcolormesh(X, Y, df)
ax.set_title("FFT")
ax.set_aspect("equal")

plt.show()
