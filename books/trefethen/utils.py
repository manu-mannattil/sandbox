import numpy as np

def cheb(N):
    """
    Compute the Chebyshev differentiation matrix and nodes.

    Based on Trefethen, *Spectral Methods in MATLAB*.

    Parameters
    ----------
    N : int
        Polynomial degree.

    Returns
    -------
    D : (N+1, N+1) ndarray
        Differentiation matrix.
    x : (N+1,) ndarray
        Chebyshev nodes.
    """
    k = np.arange(N + 1)

    # Chebyshev nodes
    x = -np.cos(np.pi * k / N)
    if N % 2 == 0:
        x[N // 2] = 0.0  # enforce exact zero for symmetry

    # Coefficients with alternating signs
    c = np.ones(N + 1)
    c[[0, -1]] = 2
    c *= (-1) ** k
    c = c[:, None]  # column vector

    # Pairwise differences matrix
    X = np.tile(x[:, None], (1, N + 1))
    dX = X - X.T

    # Differentiation matrix (off-diagonal entries)
    D = (c @ (1 / c).T) / (dX + np.eye(N + 1))

    # Set diagonal entries so each row sums to zero
    D -= np.diag(D.sum(axis=1))

    return D, x

def chebfft(v):
    """
    Compute the Chebyshev differentiation of a vector using FFT.

    Reference:
        Trefethen, "Spectral Methods in MATLAB"

    NOTE: x is from 1 to -1.
    """
    v = np.asarray(v)
    N = len(v) - 1

    if N == 0:
        return 0.0

    # Chebyshev grid
    x = np.cos(np.pi * np.arange(N + 1) / N)

    # Construct extended vector for FFT
    V = np.concatenate([v, v[1:N][::-1]])

    # FFT and real part
    U = np.real(np.fft.fft(V))

    # Wave numbers
    k = np.concatenate([np.arange(N), [0], np.arange(1 - N, 0)])

    # Differentiate in Fourier space
    W_hat = 1j * k * U
    W = np.real(np.fft.ifft(W_hat))

    # Initialize result
    w = np.zeros(N + 1)

    # Interior points
    w[1:N] = -W[1:N] / np.sqrt(1 - x[1:N] ** 2)

    # Boundary points
    ii = np.arange(N)
    w[0] = np.sum(ii**2 * U[ii]) / N + 0.5 * N * U[N]
    w[N] = (
        np.sum((-1) ** (ii + 1) * ii**2 * U[ii]) / N
        + 0.5 * (-1) ** (N + 1) * N * U[N]
    )

    return w
