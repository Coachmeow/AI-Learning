import math


def cross_entropy_with_grad(logits, target):
    """(loss, grad) of the softmax cross-entropy for one example, stable for large logits."""
    m = max(logits)
    s = sum(math.exp(z - m) for z in logits)
    loss = m + math.log(s) - logits[target]
    grad = [math.exp(z - m) / s for z in logits]
    grad[target] -= 1.0
    return loss, grad
