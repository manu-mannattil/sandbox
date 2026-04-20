"""Solve u_xx = exp(4x), u(-1) = u(1) = 0."""

import numpy as np
import matplotlib.pyplot as plt
from utils import *

xx = np.linspace(-1, 1, 100)
plt.plot(xx, (np.exp(4*xx) - xx*np.sinh(4) - np.cosh(4))/16, "b-", label="exact")

N = 20

D, x = cheb(N)
D2 = D.dot(D)
D2 = D2[1:-1, 1:-1]

v = np.exp(4*x[1:-1])
u = np.linalg.solve(D2, v)
u = np.concatenate(([0], u, [0])) # insert the BC points

plt.plot(x, u, "ko", label="grid")
plt.plot(xx, np.polyval(np.polyfit(x, u, N), xx), "r--", label="polyfit")

plt.legend()
plt.show()
