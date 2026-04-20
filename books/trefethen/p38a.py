"""Solve u_xxxx = exp(x), u(-1) = -1, u(1) = 2, u_xx(-1) + 5u_x(-1) = 3, u_xxx(1) + 7u_xx(1) = -4.

Unlike the example in the book, we're using the tau method and the BCs are complicated.
"""

import numpy as np
import matplotlib.pyplot as plt
from utils import *

xx = np.linspace(-1, 1, 100)
N = 20

D, x = cheb(N)
D2 = D@D
D3 = D2@D
D4 = D3@D

D4[0, :] = 0; D4[0, 0] = 1
D4[1] = 5*D[0] + D2[0]

D4[-1, :] = 0; D4[-1, -1] = 1
D4[-2] = D3[-1] + 7*D2[-1]

v = np.exp(x)
v[0] = -1; v[-1] = 2 # Dirichlet BC
v[1] = 3; v[-2] = -4 # Nonstandard BC
u = np.linalg.solve(D4, v)

plt.title(r"u")
plt.plot(x, u, "ko", label="grid")
plt.plot(xx, np.polyval(np.polyfit(x, u, N), xx), "r--", label="polyfit")

plt.figure()
plt.title(r"5*u_x + u_xx")
plt.plot(x, (5*D + D2)@u, "ko", label="grid")
plt.plot(xx, np.polyval(np.polyfit(x, (5*D + D2)@u, N), xx), "r--", label="polyfit")
plt.legend()

plt.figure()
plt.title(r"7*u_xx + u_xxx")
plt.plot(x, (D3 + 7*D2)@u, "ko", label="grid")
plt.plot(xx, np.polyval(np.polyfit(x, (D3 + 7*D2)@u, N), xx), "r--", label="polyfit")
plt.legend()

plt.show()
