# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.integrate import solve_ivp, cumulative_trapezoid
from scipy.optimize import root

from battery import *

b1 = BatteryInfo("data/2026-02-18.dat")
_, x, R = b1.get_field("resistance")
t, _, u = b1.get_field("current_avg")

x, R, u = x*1e-2, R*1e-6, u*1e-6

# Estimate max charge in mAH; 1 mAh = 3.6 C.
# Google 6 has max. capacity of 4614 mAh.
Q = np.trapezoid(u, t) 
print(f"Q = {Q/3.6} mAh") 

cs = CubicSpline(x, R)

def ohm(x):
    return cs(x)

def dohm(x):
    return cs(x, 1)

def f(t, q):
    x, p = q
    return [-p/(2*Q*Q*ohm(x)), -dohm(x)*p*p/(4*Q*Q*ohm(x)*ohm(x))]

def P_total(t, u, R):
    """Cumulative energy dissipated (in kWh)."""
    P = u**2 * R
    return 1e-6/3.6*cumulative_trapezoid(P, t, initial=0)

def valuef(P):
    return P[-1] - P

T = t.max()
x0 = x.min()
xT = x.max()
dt = 0.01*T

def rooteq(p0):
    """Return final x(T)."""
    sol = solve_ivp(f, [0, T], [x0, p0[0]], max_step=dt)
    return sol.y[0][-1] - xT

r = root(rooteq, [-1])
p0 = r.x[0]
sol = solve_ivp(f, [0, T], [x0, p0], max_step=dt)

t_opt, x_opt, p_opt = sol.t, sol.y[0], sol.y[1]
R_opt = ohm(x_opt)
u_opt = -p_opt/(2*R_opt*Q)
P_opt = P_total(t_opt, u_opt, R_opt)

t_const, x_const = t_opt, x_opt[0] + (x_opt[-1] - x_opt[0])*t_opt/T
u_const = np.ones(len(t_opt)) * Q/T
P_const = P_total(t_const, u_const, ohm(x_const))

P = P_total(t, u, R)

plt.plot(x*100, u, "C0", zorder=-10, label="measured")
plt.plot(x_const*100, u_const, "k--", zorder=-100, label="constant")
plt.plot(x_opt*100, u_opt, "C3", label="optimal")
plt.xlabel(r"state of charge $\xi$ (%)")
plt.ylabel(r"current I (A)")
plt.title("current")
plt.legend()

plt.figure()
plt.plot(x*100, P, "C0", label="measured")
plt.plot(x_const*100, P_const, "k--", zorder=-100, label="constant")
plt.plot(x_opt*100, P_opt, "C3", label="optimal")
plt.xlabel(r"state of charge $\xi$ (%)")
plt.ylabel(r"energy loss (kWh)")
plt.title("energy loss")
plt.legend()

plt.show()
