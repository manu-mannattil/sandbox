#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from utils import *

L = 10
N = 2**10
x = np.linspace(-L, L, N)
dx = x[1] - x[0]

# FFTW result.
K_phi = load_array("conv1d.bin", N)
plt.plot(x, K_phi.real, "k", label="FFTW")

# Compare with exact.
alpha, beta = 1.0, 0.5
a, b = -4.0, 3.0
gamma = alpha*beta/(alpha+beta)
delta = a + b
K_phi_exact = np.sqrt(np.pi*gamma/(alpha*beta))*np.exp(-gamma*(x-delta)**2)
plt.plot(x, K_phi_exact, "r--", label="exact")

plt.legend()
plt.show()
