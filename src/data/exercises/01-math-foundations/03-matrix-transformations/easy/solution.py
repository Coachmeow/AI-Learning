def apply(M, points):
    """Multiply the 2x2 matrix M by every point [x, y] and return the new points."""
    out = []
    for x, y in points:
        out.append([M[0][0] * x + M[0][1] * y, M[1][0] * x + M[1][1] * y])
    return out
