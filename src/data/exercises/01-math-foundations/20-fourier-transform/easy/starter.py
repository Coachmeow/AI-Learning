import math


def hann_window(N):
    """w[n] = 0.5 * (1 - cos(2*pi*n / (N - 1))) for n = 0 .. N-1."""
    if N == 1:
        return [1.0]
    return [1.0] * N  # TODO: the Hann formula for each n in range(N)
