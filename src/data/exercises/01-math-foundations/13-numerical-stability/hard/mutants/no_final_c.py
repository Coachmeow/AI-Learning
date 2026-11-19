def neumaier_sum(xs):
    """Sum of xs with Neumaier's compensated summation."""
    s = 0.0
    c = 0.0
    for x in xs:
        t = s + x
        if abs(s) >= abs(x):
            c += (s - t) + x
        else:
            c += (x - t) + s
        s = t
    return s
