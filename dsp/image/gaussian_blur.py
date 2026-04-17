"""Gaussian blurring an image."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread

def imread_bw(name):
    """Read an image and average RGB values to produce a grayscale image."""
    im = imread(name)
    if len(im.shape) > 2:
        im = np.sum(im, axis=2)/3
    return im

# There would be border issues because the image isn't exactly periodic.
image = imread_bw("samples/tiger.jpg")

# There would be border issues because the image isn't exactly periodic.
# image = imread_bw("board.png")

# This image creates problems because it's not at all periodic and leads
# to terrible results.
# image = imread_bw("gradient.png")

# Domain setup.
n = image.shape[0]
x = np.linspace(-n/2, n/2, n)
dx = x[1] - x[0]
X, Y = np.meshgrid(x, x)

# Set up the blurring kernel.
# Image will be smeared along the horizontal axis.
# Too small a radius will create problems.
r1 = 10
r2 = 1
K = np.exp(-(X**2/(2*r1**2) + Y**2/(2*r2**2)))
K /= np.sqrt(2 * np.pi * r1**2) # normalization
K /= np.sqrt(2 * np.pi * r2**2) # normalization

# DFTs assume that the "origin" of the kernel are at the "ends".
# But the kernel we've defined above has an origin at the center.
# So shift appropriately to put the origin at the "ends."
K = np.fft.fftshift(K)
# The multiplication by dx^d is to turn a discrete DFT sum into
# an integral.
K_q = np.fft.fftn(K) * (dx**2)

image_q = np.fft.fftn(image)
image_blur = np.fft.ifftn(image_q * K_q).real

plt.axis("off")
plt.imshow(image_blur, cmap="binary_r")
plt.show()
