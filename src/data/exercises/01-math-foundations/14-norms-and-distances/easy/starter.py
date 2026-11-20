import math


def cosine_similarity(a, b):
    """Cosine of the angle between vectors a and b."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    # TODO: divide the dot product by the product of the two norms
    raise NotImplementedError
