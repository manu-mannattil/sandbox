 # -*- coding: utf-8 -*-

"""Optimal charging of a lead-acid battery.

Reproduces Fig. 7 of Parvini & Vahidi, IEEE, 2015.
https://doi.org/10.1109/ACC.2015.7170755
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.optimize import root

Q = 19.7
alpha = 1

def R(x):
    return 0.098*x*x - 0.12*x + 0.061

def dR(x):
    return 0.196*x - 0.12

def f(t, q):
    x, p = q
    return [-p/(2*Q*Q*R(x)), -dR(x)*p*p/(4*Q*Q*R(x)*R(x))]

T = 1
x0 = 0
xT = 1
dt = 0.001

def rooteq(p0):
    """Return final x(T)."""
    sol = solve_ivp(f, [0, T], [x0, p0[0]], max_step=dt)
    return sol.y[0][-1] - xT

r = root(rooteq, [-1])
p0 = r.x[0]
sol = solve_ivp(f, [0, T], [x0, p0], max_step=dt)

plt.figure()
plt.plot(sol.t, sol.y[0])
plt.xlabel(r"time (hours)")
plt.ylabel(r"state of charge")

plt.figure()
plt.plot(sol.t, sol.y[1])
plt.xlabel(r"time (hours)")
plt.ylabel(r"$\lambda$")

plt.figure()
x, p = sol.y[0], sol.y[1]
u = -p/(2*R(x)*Q)
plt.plot(sol.t, u)
plt.xlabel(r"time (hours)")
plt.ylabel(r"charging current (A)")

plt.show()
