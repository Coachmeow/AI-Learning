def median(xs):
    """The middle value of xs, or the mean of the two middle values."""
    s = list(xs)
    n = len(s)
    mid = n // 2
    if n % 2 == 1:
        return s[mid]
    return (s[mid - 1] + s[mid]) / 2
