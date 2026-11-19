import math
from collections import Counter


def mutual_information(xs, ys):
    """Mutual information in bits of paired samples, from their empirical joint distribution."""
    raise NotImplementedError


def rank_features(features, target):
    """[(name, mi), ...] from highest to lowest MI with the target; ties by name."""
    raise NotImplementedError
