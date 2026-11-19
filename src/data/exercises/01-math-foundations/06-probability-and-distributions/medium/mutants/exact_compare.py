import math


def analyze_joint(joint):
    """(px, py, independent) for a joint table joint[i][j] = P(X = i, Y = j)."""
    if any(c < 0 for row in joint for c in row):
        raise ValueError("probabilities can't be negative")
    px = [sum(row) for row in joint]
    if abs(sum(px) - 1) > 1e-9:
        raise ValueError("the table must add up to 1")
    py = [sum(row[j] for row in joint) for j in range(len(joint[0]))]
    independent = all(
        joint[i][j] == px[i] * py[j]
        for i in range(len(px)) for j in range(len(py))
    )
    return px, py, independent
