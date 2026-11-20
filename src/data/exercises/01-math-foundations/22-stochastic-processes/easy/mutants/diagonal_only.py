def step_distribution(dist, P):
    """Distribution after one step: new[j] = sum over i of dist[i] * P[i][j]."""
    n = len(dist)
    new = []
    for j in range(n):
        new.append(dist[j] * P[j][j])
    return new
