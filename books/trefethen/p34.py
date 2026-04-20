"""Allen-Cahn equation with Dirichlet BC."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from utils import *

N = 20
D, x = cheb(N)
D2 = D@D

# We delete the top/bottom row to ensure that the boundary values are
# unaffected during each update.  We don't have to impose u[0] = -1, u[-1]
# = 1 during the update step because u - u^3 = 0 at the boundaries with these
# initial conditions.  Alternatively, impose u[0] = -1, u[-1] = 1 during each
# update step.
D2[0] = np.zeros(N + 1)
D2[-1] = np.zeros(N + 1)

eps = 0.01
dt = 0.01

u = 0.53*x + 0.47*np.sin(-1.5*np.pi*x)
xx = np.linspace(-1, 1, 100)

fig, ax = plt.subplots()
t = 0
ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$u(x)$")
ax.set_ylim(-1.5, 1.5)
uu = np.polyval(np.polyfit(x, u, N), xx)
line, = ax.plot(xx, uu)

def animate(i):
    global u
    u += dt*(eps*D2@u + u - u**3)
    uu = np.polyval(np.polyfit(x, u, N), xx)
    line.set_ydata(uu)
    return line,

ani = FuncAnimation(fig, animate, frames=1, interval=1, blit=True)
plt.show()
