import math


def perplexity(pairs):
    """e ** (mean cross-entropy in nats) over (true_index, logits) pairs."""
    if not pairs:
        raise ValueError("perplexity needs at least one token")
    total = 0.0
    for true_index, logits in pairs:
        lse = math.log(sum(math.exp(z) for z in logits))
        total += lse - logits[true_index]
    return math.exp(total / len(pairs))
