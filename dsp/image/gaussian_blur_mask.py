"""Masked blurring.

This script demonstrates masked blurring.  Basically, you're allowed to
load a black-and-white mask that will determine the blur radius: black
= largest blur radius, white = smallest.
"""

import cv2
import matplotlib.pyplot as plt
import numpy as np

def imread_bw(name, size=None, rescale=False):
    """Read an image and average RGB values to produce a grayscale image."""
    im = cv2.imread(name)
    if size:
        im = cv2.resize(im, dsize=(size, size), interpolation=cv2.INTER_LINEAR)

    if len(im.shape) > 2:
        im = np.sum(im, axis=2) / 3

    if rescale:
        return (im - np.min(im)) / (np.max(im) - np.min(im))
    else:
        return im

def blur(image, r=1):
    """Blur an image with a given radius."""
    n = image.shape[0]
    x = np.linspace(-n / 2, n / 2, n)
    dx = x[1] - x[0]
    X, Y = np.meshgrid(x, x)

    # Set up the blurring kernel.
    K = np.exp(-(X**2 / (2 * r**2) + Y**2 / (2 * r**2)))
    K /= (2 * np.pi * r**2) # normalization

    # DFTs assume that the "origin" of the kernel are at the "ends".
    # But the kernel we've defined above has an origin at the center.
    # So shift appropriately to put the origin at the "ends."
    K = np.fft.fftshift(K)
    # The multiplication by dx^d is to turn a discrete DFT sum into
    # an integral.
    K_q = np.fft.fftn(K) * (dx**2)

    image_q = np.fft.fftn(image)
    return np.fft.ifftn(image_q * K_q).real

steps = 100
r_min, r_max = 1, 20
r = np.linspace(r_min, r_max, steps)

mask = r_min + (r_max-r_min) * (1 - imread_bw("samples/grad.png", size=512, rescale=True))
image = imread_bw("samples/tiger.jpg")
n = image.shape[0]

blur_list = []
for i in range(steps):
    blur_list.append(blur(image, r[i]))

coeff = []
for i in range(steps):
    coeff.append(np.zeros((n, n)))

for i in range(n):
    for j in range(n):
        k = np.searchsorted(r, mask[i][j])
        if k <= 0:
            coeff[0][i][j] = 1.0
        elif k >= steps:
            coeff[-1][i][j] = 1.0
        else:
            coeff[k - 1][i][j] = (r[k] - mask[i][j]) / (r[k] - r[k - 1])
            coeff[k][i][j] = (mask[i][j] - r[k - 1]) / (r[k] - r[k - 1])

image_blur = np.zeros((n, n))
for i in range(steps):
    image_blur += blur_list[i] * coeff[i]

plt.axis("off")
plt.imshow(image_blur, cmap="binary_r")
plt.show()
