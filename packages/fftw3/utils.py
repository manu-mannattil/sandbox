# -*- coding: utf-8 -*-

import numpy as np
import struct

def load_array(name):
    """Load a complex fftw array saved to a binary file."""
    header = "=ii"
    with open(name, "rb") as fd:
        N, dim = struct.unpack(header, fd.read(struct.calcsize(header)))
        a = np.fromfile(fd, dtype=np.double)
        a = a[::2] + 1j * a[1::2] # separate real and complex parts
        a = a.reshape((N,) * dim)
        return a
