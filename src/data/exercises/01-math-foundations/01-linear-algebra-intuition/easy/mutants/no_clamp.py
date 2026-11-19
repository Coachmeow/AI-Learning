import math


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def magnitude(a):
    return sum(x * x for x in a) ** 0.5


def cosine_similarity(a, b):
    return dot(a, b) / (magnitude(a) * magnitude(b))


def angle_between(a, b):
    return math.degrees(math.acos(cosine_similarity(a, b)))
