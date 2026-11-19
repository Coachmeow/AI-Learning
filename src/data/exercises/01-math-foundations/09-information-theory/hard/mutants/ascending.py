import math
from collections import Counter


def mutual_information(xs, ys):
    """Mutual information in bits of paired samples, from their empirical joint distribution."""
    if len(xs) != len(ys) or not xs:
        raise ValueError("xs and ys must be non-empty and the same length")
    n = len(xs)
    pxy, px, py = Counter(zip(xs, ys)), Counter(xs), Counter(ys)
    mi = 0.0
    for (x, y), c in pxy.items():
        p = c / n
        mi += p * math.log2(p / ((px[x] / n) * (py[y] / n)))
    return mi


def rank_features(features, target):
    """[(name, mi), ...] from highest to lowest MI with the target; ties by name."""
    scores = [(name, mutual_information(col, target)) for name, col in features.items()]
    return sorted(scores, key=lambda t: (t[1], t[0]))
