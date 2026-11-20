import cmath


def _fft(x):
    N = len(x)
    if N == 1:
        return [complex(x[0])]
    even = _fft(x[0::2])
    odd = _fft(x[1::2])
    out = [0j] * N
    for k in range(N // 2):
        t = cmath.exp(-2j * cmath.pi * k / N) * odd[k]
        out[k] = even[k] + t
        out[k + N // 2] = even[k] - t
    return out


def fft(x):
    """Radix-2 Cooley-Tukey FFT; len(x) must be a power of 2."""
    N = len(x)
    return _fft(list(x))
