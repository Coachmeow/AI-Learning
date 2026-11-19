import math


def clip_by_norm(grads, max_norm):
    """Scale grads so their norm is at most max_norm, keeping the direction."""
    total_norm = math.sqrt(sum(g * g for g in grads))
    if total_norm > max_norm:
        pass  # TODO: return every g scaled by max_norm / total_norm
    return list(grads)
