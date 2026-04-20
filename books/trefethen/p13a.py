"""Solve u_xx = exp(4x), u(-1) = alpha, u(1) = beta (using the tau method)."""

import numpy as np
import matplotlib.pyplot as plt
from utils import *

# Boundary conditions.
alpha = 0
beta = 0

xx = np.linspace(-1, 1, 100)
plt.plot(xx, (np.exp(4*xx) - xx*np.sinh(4) - np.cosh(4))/16, "b-", label="exact")

N = 20

D, x = cheb(N)
D2 = D.dot(D)
D2[0, :] = 0
D2[-1, :] = 0
D2[0, 0] = 1
D2[-1, -1] = 1

v = np.exp(4*x)
v[0] = alpha
v[-1] = beta
u = np.linalg.solve(D2, v)

plt.plot(x, u, "ko", label="grid")
plt.plot(xx, np.polyval(np.polyfit(x, u, N), xx), "r--", label="polyfit")

plt.legend()
plt.show()
