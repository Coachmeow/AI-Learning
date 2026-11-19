def broadcast_shape(a, b):
    """The NumPy broadcast result of shapes a and b; ValueError if incompatible."""
    n = min(len(a), len(b))
    a = tuple(a)[len(a) - n:]
    b = tuple(b)[len(b) - n:]
    out = []
    for x, y in zip(a, b):
        if x == y or y == 1:
            out.append(x)
        elif x == 1:
            out.append(y)
        else:
            raise ValueError(f"sizes {x} and {y} can't be broadcast")
    return tuple(out)
