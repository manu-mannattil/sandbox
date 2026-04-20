#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from utils import *

L = 10
N = 1024
s = 1
k = 2*np.pi*np.fft.fftfreq(N, d=2*L/(N-1))
k = np.fft.fftshift(k)

x = np.linspace(-L, L, N)
y = np.exp(-s*x*x)
print(y.mean())

# PSD using NumPy FFT.
yq = np.fft.fft(y)
yq = np.fft.fftshift(yq)/N
plt.plot(k, 2*L*np.abs(yq), "b-", label="NumPy")

# PSD using FFTW.
a = load_array("1dgauss.bin")
a = np.fft.fftshift(a)/N
plt.plot(k, 2*L*np.abs(a), "r--", label="FFTW")

# Analytical result.
b = np.sqrt(np.pi/s) * np.exp(-k**2/(4*s))
plt.plot(k, b, label="exact")

plt.xlim(-25, 25)
plt.legend()
plt.show()
