#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from utils import *

L = 10
N = 1024
s = 1

a = load_array("1dgauss-deriv.bin")
x = np.linspace(-L, L, N)
y = -2*s*x*np.exp(-s*x*x)

plt.plot(a.real)
plt.plot(y)
plt.show()
