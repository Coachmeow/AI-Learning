def neumaier_sum(xs):
    """Sum of xs with Neumaier's compensated summation."""
    s = 0.0
    c = 0.0
    for x in xs:
        y = x - c
        t = s + y
        c = (t - s) - y
        s = t
    return s
