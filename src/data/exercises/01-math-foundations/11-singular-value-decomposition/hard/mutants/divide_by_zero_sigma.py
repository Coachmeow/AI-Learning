import math


def svd2(A):
    """(U, S, Vt) of a 2x2 matrix A, with U and Vt as lists of rows and S = [s1, s2], s1 >= s2 >= 0."""
    (a, b), (c, d) = A
    p, q, r = a * a + c * c, a * b + c * d, b * b + d * d
    mid = (p + r) / 2
    spread = math.sqrt(((p - r) / 2) ** 2 + q * q)
    lam1, lam2 = mid + spread, max(mid - spread, 0.0)
    if abs(q) > 1e-12:
        x, y = q, lam1 - p
        length = math.hypot(x, y)
        v1 = [x / length, y / length]
    else:
        v1 = [1.0, 0.0] if p >= r else [0.0, 1.0]
    v2 = [-v1[1], v1[0]]
    s1, s2 = math.sqrt(lam1), math.sqrt(lam2)

    def apply(v, s):
        return [(a * v[0] + b * v[1]) / s, (c * v[0] + d * v[1]) / s]

    u1 = apply(v1, s1) if s1 > 1e-12 else [1.0, 0.0]
    u2 = apply(v2, s2)
    U = [[u1[0], u2[0]], [u1[1], u2[1]]]
    return U, [s1, s2], [v1, v2]
