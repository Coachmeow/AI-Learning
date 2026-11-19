import math


def cross_entropy_with_grad(logits, target):
    """(loss, grad) of the softmax cross-entropy for one example, stable for large logits."""
    m = max(logits)
    for i in range(len(logits)):
        logits[i] -= m
    m = 0.0
    s = sum(math.exp(z - m) for z in logits)
    loss = m + math.log(s) - logits[target]
    grad = [math.exp(z - m) / s for z in logits]
    grad[target] -= 1.0
    return loss, grad
