import math


def softmax(logits):
    """Probabilities from logits, safe for large logits."""
    m = max(logits)
    exps = []  # TODO: math.exp(z - m) for every z in logits
    total = sum(exps)
    return [e / total for e in exps]
