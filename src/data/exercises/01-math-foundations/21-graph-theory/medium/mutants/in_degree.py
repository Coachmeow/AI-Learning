def pagerank(n, edges, d=0.85, tol=1e-12, max_iter=1000):
    """PageRank scores for nodes 0..n-1; edges are (u, v) pairs, u -> v."""
    out_degree = [0] * n
    for _, v in edges:
        out_degree[v] += 1
    score = [1 / n] * n
    for _ in range(max_iter):
        dangling = sum(score[u] for u in range(n) if out_degree[u] == 0)
        new = [(1 - d) / n + d * dangling / n] * n
        for u, v in edges:
            new[v] += d * score[u] / out_degree[u]
        change = sum(abs(a - b) for a, b in zip(new, score))
        score = new
        if change < tol:
            break
    return score
