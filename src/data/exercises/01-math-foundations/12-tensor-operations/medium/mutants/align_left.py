def broadcast_shape(a, b):
    """The NumPy broadcast result of shapes a and b; ValueError if incompatible."""
    n = max(len(a), len(b))
    a = tuple(a) + (1,) * (n - len(a))
    b = tuple(b) + (1,) * (n - len(b))
    out = []
    for x, y in zip(a, b):
        if x == y or y == 1:
            out.append(x)
        elif x == 1:
            out.append(y)
        else:
            raise ValueError(f"sizes {x} and {y} can't be broadcast")
    return tuple(out)
