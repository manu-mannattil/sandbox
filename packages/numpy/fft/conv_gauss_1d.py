#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

L = 10
N = 2**10
x = np.linspace(-L, L, N)
dx = x[1] - x[0]

alpha, beta = 1.0, 0.5
a, b = -4.0, 3.0

# Kernel is an off-centered Gaussian.
K = np.exp(-alpha*(x - a)**2)

# DFTs assume that the "origin" of the kernel at the "ends".
# But the kernel we've defined above has an origin at the center.
# So shift appropriately to put the origin at the "ends."
K = np.fft.fftshift(K)

# Function.
f = np.exp(-beta*(x - b)**2)

# FT of convolution is product of FTs.
Kq = np.fft.fft(K)
fq = np.fft.fft(f)
print(fq[:10])
Kfq = Kq*fq
# We need to also multiply by dx to make the sum an integral.
Kfq = Kfq*dx

# Take inverse transform of FT of convolution to get convolution in real space.
Kf = np.fft.ifft(Kfq)
plt.plot(x, Kf.real, "k-", label="FFT")

# Compare with exact.
gamma = alpha*beta/(alpha+beta)
delta = a + b
Kf_exact = np.sqrt(np.pi*gamma/(alpha*beta))*np.exp(-gamma*(x-delta)**2)
plt.plot(x, Kf_exact, "r--", label="exact")

plt.legend()
plt.show()
