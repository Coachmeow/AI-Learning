def cmul(z, w):
    """Multiply complex numbers given as (real, imag) tuples."""
    a, b = z
    c, d = w
    return (a * c - b * d, a * d - b * c)
