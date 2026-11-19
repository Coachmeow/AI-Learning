def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def sub(a, b):
    return [x - y for x, y in zip(a, b)]


def scale(a, s):
    return [x * s for x in a]


def magnitude(a):
    return dot(a, a) ** 0.5


def gram_schmidt(vectors):
    basis = []
    for v in vectors:
        w = list(v)
        for u in basis:
            w = sub(w, scale(u, dot(w, u)))
        basis.append(scale(w, 1 / magnitude(w)))
    return basis
