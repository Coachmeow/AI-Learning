def top_p_filter(probs, p):
    """[(index, renormalized prob), ...]: the smallest set of top tokens whose probability reaches p."""
    order = sorted(range(len(probs)), key=lambda i: (-probs[i], i))
    kept = []
    cumulative = 0.0
    for i in order:
        cumulative += probs[i]
        if cumulative >= p:
            break
        kept.append(i)
    if not kept:
        kept = [order[0]]
    total = sum(probs[i] for i in kept)
    return [(i, probs[i] / total) for i in kept]
