"""Solve u_xxxx = exp(x), u(-1) = u(1) = u_x(-1) = u_x(1) = 0.

Unlike the example in the book, we're using the tau method.
"""

import numpy as np
import matplotlib.pyplot as plt
from utils import *

xx = np.linspace(-1, 1, 100)
N = 20

D, x = cheb(N)
D4 = D@D@D@D

D4[0, :] = 0; D4[0, 0] = 1
D4[1] = D[0]

D4[-1, :] = 0; D4[-1, -1] = 1
D4[-2] = D[-1]

v = np.exp(x)
v[0] = 0; v[1] = 0
v[-1] = 0; v[-2] = 0
u = np.linalg.solve(D4, v)

plt.plot(x, u, "ko", label="grid")
plt.plot(xx, np.polyval(np.polyfit(x, u, N), xx), "r--", label="polyfit")

plt.legend()
plt.show()
