def circular_convolution(x, h):
    """y[n] = sum over k of h[k] * x[(n - k) % N]; x and h have length N."""
    N = len(x)
    if len(h) != N:
        raise ValueError("x and h must have the same length")
    return [sum(h[k] * x[(n - k) % N] for k in range(N)) for n in range(N)]


def linear_convolution(x, h):
    """Convolution without wraparound, of length len(x) + len(h) - 1."""
    L = max(len(x), len(h))
    return circular_convolution(list(x) + [0] * (L - len(x)), list(h) + [0] * (L - len(h)))
