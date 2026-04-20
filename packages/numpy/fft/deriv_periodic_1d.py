# -*- coding: utf-8 -*-
#
# Computes the derivative of phi(x) = sin(2x) + cos(5x) using FFT.
# Adapted from https://scicomp.stackexchange.com/a/36172
#

import numpy as np
import matplotlib.pyplot as plt

# Number of points.
N = 1024

# FFTs assume that the input signal is periodic.  Our test function
#   phi(x) = sin(2x) + cos(5x).
# Although this function is periodic in the interval [0, 2pi], the end
# point 0 and 2pi correspond to the exact same point.  So we remove the
# last (N + 1)th point.
x = np.linspace(0, 2 * np.pi, N + 1)
x = x[:-1]

dx = x[1] - x[0]
f = np.sin(2 * x) + np.cos(5 * x)

# Frequencies need to be multiplied by 2*np.pi to get usual physics
# conventions.
q = 2 * np.pi * np.fft.fftfreq(N, dx)

df = np.fft.ifft(1j * q * np.fft.fft(f)).real
plt.plot(x, df, "k", label="FFT")

# Compare with exact.
df_exact = 2 * np.cos(2 * x) - 5 * np.sin(5 * x)
plt.plot(x, df_exact, "r--", label="exact")

plt.legend()
plt.show()
