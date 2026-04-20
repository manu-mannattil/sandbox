"""Chebyshev differentiation of a smooth function."""

import numpy as np
import matplotlib.pyplot as plt
from utils import *

xx = np.linspace(-1, 1, 100)
plt.plot(xx, np.exp(xx)*(np.sin(5*xx) + 5*np.cos(5*xx)), "b-", label="exact")

N = 10
D, x = cheb(N)
v = np.exp(x)*np.sin(5*x)
w = D.dot(v)

plt.plot(x, w, "ko", label="grid")
plt.plot(xx, np.polyval(np.polyfit(x, w, N), xx), "r--", label="polyfit")

plt.title("u'(x) = exp(x)[sin(x) + 5cos(x)]")
plt.legend()
plt.show()
