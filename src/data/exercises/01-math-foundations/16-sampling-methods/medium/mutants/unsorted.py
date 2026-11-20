def top_p_filter(probs, p):
    """[(index, renormalized prob), ...]: the smallest set of top tokens whose probability reaches p."""
    order = list(range(len(probs)))
    kept = []
    cumulative = 0.0
    for i in order:
        kept.append(i)
        cumulative += probs[i]
        if cumulative >= p:
            break
    total = sum(probs[i] for i in kept)
    return [(i, probs[i] / total) for i in kept]
