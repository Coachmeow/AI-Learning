def step_distribution(dist, P):
    """Distribution after one step: new[j] = sum over i of dist[i] * P[i][j]."""
    n = len(dist)
    new = []
    for j in range(n):
        new.append(sum(P[i][j] for i in range(n)) / n)
    return new
