# -*- coding: utf-8 -*-

"""Solves the 1D wave equation using Fourier differentiation.

    u_tt = u_xx     x in [-1, 1]

The solution is periodic and wraps around.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def fftfreq(x):
    """Return properly scaled wavenumbers."""
    return np.fft.fftfreq(len(x), d=(x[1] - x[0])/(2*np.pi))

N = 128
x = np.linspace(-1, 1, N)
q = fftfreq(x)

# Time step.
dt = 1e-3

# Initial perturbation is a Gaussian.
u = np.exp(-100*x*x)
# In the past, let's put the wave to the right of the origin.
# So, this is a leftward moving wave.
u_old = np.exp(-100*(x - dt)*(x - dt))

fig, ax = plt.subplots()
ax.set_title("1d wave equation using FFT")
ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$u(x)$")
ax.set_ylim(-0.5, 1.5)

line, = ax.plot(x, u)

def animate(i):
    global u, u_old

    # Use Fourier differentiation to find u_xx.
    u_q = np.fft.fft(u)
    u_xx = np.fft.ifft(-q*q*u_q).real

     

    # Leapfrog integration in real space.
    u_new = 2*u - u_old + dt**2*u_xx
    u_old = u
    u = u_new

    line.set_ydata(u)
    return line,

ani = FuncAnimation(fig, animate, frames=1, interval=1, blit=True)
plt.show()
