import math


def entropy(probs):
    """Entropy of a distribution, in bits."""
    return -sum(p * math.log(p) for p in probs if p > 0)
