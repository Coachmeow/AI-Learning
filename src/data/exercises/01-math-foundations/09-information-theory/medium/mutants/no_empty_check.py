import math


def perplexity(pairs):
    """e ** (mean cross-entropy in nats) over (true_index, logits) pairs."""
    total = 0.0
    for true_index, logits in pairs:
        m = max(logits)
        lse = m + math.log(sum(math.exp(z - m) for z in logits))
        total += lse - logits[true_index]
    return math.exp(total / len(pairs))
