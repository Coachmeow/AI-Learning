def classify(f, x, y, h=1e-4):
    """'minimum', 'maximum', 'saddle' or 'unknown' for the critical point (x, y) of f(x, y).

    Raises ValueError if (x, y) is not a critical point.
    """
    gx = (f(x + h, y) - f(x - h, y)) / (2 * h)
    gy = (f(x, y + h) - f(x, y - h)) / (2 * h)
    if max(abs(gx), abs(gy)) > 1e-6:
        raise ValueError("not a critical point: the gradient is not zero")
    fxx = (f(x + h, y) - 2 * f(x, y) + f(x - h, y)) / (h ** 2)
    fyy = (f(x, y + h) - 2 * f(x, y) + f(x, y - h)) / (h ** 2)
    fxy = (f(x + h, y + h) - f(x + h, y - h) - f(x - h, y + h) + f(x - h, y - h)) / (4 * h ** 2)
    if fxx > 1e-6 and fyy > 1e-6:
        return "minimum"
    if fxx < -1e-6 and fyy < -1e-6:
        return "maximum"
    if fxx * fyy < -1e-12:
        return "saddle"
    return "unknown"
