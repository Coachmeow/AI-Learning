def broadcast_shape(a, b):
    """The NumPy broadcast result of shapes a and b; ValueError if incompatible."""
    n = max(len(a), len(b))
    a = (1,) * (n - len(a)) + tuple(a)
    b = (1,) * (n - len(b)) + tuple(b)
    out = []
    for x, y in zip(a, b):
        if x == y or y == 1:
            out.append(x)
        elif x == 1:
            out.append(y)
        else:
            out.append(max(x, y))
    return tuple(out)
