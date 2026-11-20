import cmath


def dft(x):
    """X[k] = sum over n of x[n] * exp(-2*pi*i*k*n/N)."""
    N = len(x)
    return [sum(complex(x[n]).real * cmath.exp(-2j * cmath.pi * k * n / N) for n in range(N)) for k in range(N)]


def idft(X):
    """x[n] = (1/N) * sum over k of X[k] * exp(+2*pi*i*k*n/N)."""
    N = len(X)
    return [sum(X[k] * cmath.exp(2j * cmath.pi * k * n / N) for k in range(N)) / N for n in range(N)]
