# -*- coding: utf-8 -*-

"""Computes the second derivative of a 1D Gaussian exp(-s*x**2)."""

import numpy as np
from scipy.fft import rfft, irfft, rfftfreq
from scipy.fft import fft, ifft, fftfreq
import matplotlib.pyplot as plt

# Make data ------------------------------------------------------------

N = 2**10
x = np.linspace(-10, 10, N)
dx = x[1] - x[0]

# Gaussian.
s = 2
f = np.exp(-s*x**2)

# FFT version ----------------------------------------------------------

# Fourier transform of Gaussian.
fq = fft(f)
q = fftfreq(N, d=dx/(2*np.pi))

# Derivative of Gaussian.
dfq = 1j*q*fq
df = ifft(dfq).real

plt.figure()
plt.title(r"Derivative with FFT")
plt.plot(x, df)
plt.plot(x, -2*x*s*f)
plt.show()

# RFFT version ---------------------------------------------------------

# Fourier transform of Gaussian.
fq = rfft(f)
q = rfftfreq(N, d=dx/(2*np.pi))

# Derivative of Gaussian.
dfq = 1j*q*fq
df = irfft(dfq).real

plt.figure()
plt.title(r"Derivative with RFFT")
plt.plot(x, df)
plt.plot(x, -2*x*s*f)
plt.show()
