def step_distribution(dist, P):
    """Distribution after one step: new[j] = sum over i of dist[i] * P[i][j]."""
    n = len(dist)
    new = []
    for j in range(n):
        new.append(sum(dist[i] * P[j][i] for i in range(n)))
    return new
