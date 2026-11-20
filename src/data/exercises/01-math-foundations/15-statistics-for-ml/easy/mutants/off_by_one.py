def median(xs):
    """The middle value of xs, or the mean of the two middle values."""
    s = sorted(xs)
    n = len(s)
    mid = n // 2
    if n % 2 == 1:
        return s[mid]
    return (s[mid] + s[mid + 1]) / 2 if mid + 1 < n else s[mid]
