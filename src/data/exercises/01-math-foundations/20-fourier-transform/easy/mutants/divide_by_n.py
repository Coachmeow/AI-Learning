import math


def hann_window(N):
    """w[n] = 0.5 * (1 - cos(2*pi*n / (N - 1))) for n = 0 .. N-1."""
    if N == 1:
        return [1.0]
    return [0.5 * (1 - math.cos(2 * math.pi * n / N)) for n in range(N)]
