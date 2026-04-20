"""Allen-Cahn equation with a time-varying Dirichlet BC."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from utils import *

N = 20
D, x = cheb(N)
D2 = D@D

eps = 0.01
dt = 0.01
t = 0

u = 0.53*x + 0.47*np.sin(-1.5*np.pi*x)
xx = np.linspace(-1, 1, 100)

fig, ax = plt.subplots()
ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$u(x)$")
ax.set_ylim(-1.5, 2.5)
uu = np.polyval(np.polyfit(x, u, N), xx)
line, = ax.plot(xx, uu)

def animate(i):
    global u, t
    t += dt
    u += dt*(eps*D2@u + u - u**3)

    # Adjust value of endpoints to match the BC.
    # Note that we don't have to modify D2 to impose BC.
    u[-1] = np.sin(t/5)**2 + 1
    u[0] = -1

    uu = np.polyval(np.polyfit(x, u, N), xx)
    line.set_ydata(uu)
    return line,

ani = FuncAnimation(fig, animate, frames=100, interval=1, blit=True)
plt.show()
