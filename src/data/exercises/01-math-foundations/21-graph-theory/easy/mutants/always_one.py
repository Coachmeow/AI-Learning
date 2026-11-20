from collections import deque


def bfs_distances(adj, start):
    """Hop distances from start to every reachable node."""
    dist = {start: 0}
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if v not in dist:
                dist[v] = 1
                queue.append(v)
    return dist
