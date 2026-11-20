def step_distribution(dist, P):
    """Distribution after one step: new[j] = sum over i of dist[i] * P[i][j]."""
    n = len(dist)
    new = []
    for j in range(n):
        new.append(0.0)  # TODO: total probability of landing in state j
    return new
