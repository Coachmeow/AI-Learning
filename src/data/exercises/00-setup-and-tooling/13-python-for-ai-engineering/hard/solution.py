import math


def _mean(values):
    return sum(values) / len(values)


def _pstd(values):
    m = _mean(values)
    return math.sqrt(sum((v - m) ** 2 for v in values) / len(values))


def make_standardizer(rows):
    """Fit column means and population stds on `rows`; return standardize(row) -> list of floats."""
    if not rows:
        raise ValueError("make_standardizer() needs at least one row")
    columns = list(zip(*rows, strict=True))
    means = [_mean(c) for c in columns]
    scales = [s if s > 0 else 1.0 for s in (_pstd(c) for c in columns)]

    def standardize(row):
        return [(v - m) / s for v, m, s in zip(row, means, scales, strict=True)]

    return standardize
