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
