import math


def softmax(logits):
    """Probabilities from logits, safe for large logits."""
    m = max(logits)
    exps = [math.exp(z) for z in logits]
    total = sum(exps)
    return [e / total for e in exps]
