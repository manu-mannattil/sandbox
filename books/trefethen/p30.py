"""Spectral integration by treating integrand as the RHS of an ODE."""

import numpy as np
from utils import *
from scipy.special import erf

N = 50
D, x = cheb(N)

x = x[1:]
w = np.linalg.inv(D[1:, 1:])[-1]

f = np.abs(x)**3
I = f.dot(w)
error = np.abs(0.5 - I)
print(f"|x|^3: I = {I}; error = {error}")

x[N//2 - 1] += 1e-20 # to avoid 1/0 error
f = np.exp(-(x**-2))
x[N//2 - 1] -= 1e-20
I = f.dot(w)
error = np.abs(2*(np.exp(-1) +  np.sqrt(np.pi)*(erf(1) - 1)) - I)
print(f"exp(-x^-2): I = {I}; error = {error}")

f = 1/(1 + x*x)
I = f.dot(w)
error = np.abs(np.pi/2 - I)
print(f"1/(1 + x^2): I = {I}; error = {error}")

f = x**10
I = f.dot(w)
error = np.abs(2/11 - I)
print(f"x^10: I = {I}; error = {error}")
