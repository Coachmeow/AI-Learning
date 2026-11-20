import cmath


def fft(x):
    """Radix-2 Cooley-Tukey FFT; len(x) must be a power of 2."""
    # Your code here
    return [complex(v) for v in x]
