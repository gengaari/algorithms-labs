import heapq
from typing import List, Tuple, Dict


def dijkstra(n: int, edges: List[Tuple[int, int, int]], start: int = 1):
    """Алгоритм Дейкстри для знаходження найкоротших шляхів від вершини start."""
    adj: Dict[int, List[Tuple[int, int]]] = {v: [] for v in range(1, n + 1)}
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))

    dist = {v: float("inf") for v in range(1, n + 1)}
    pred = {v: -1 for v in range(1, n + 1)}
    dist[start] = 0
    visited = set()
    pq = [(0, start)]

    while pq:
        d_u, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        for v, w in adj[u]:
            if v not in visited and d_u + w < dist[v]:
                dist[v] = d_u + w
                pred[v] = u
                heapq.heappush(pq, (dist[v], v))

    return pred, dist


def reconstruct_path(pred: Dict[int, int], start: int, target: int) -> str:
    """Відновлює найкоротший шлях від start до target за масивом попередників pred."""
    if target == start:
        return str(start)
    if pred.get(target, -1) == -1:
        return "немає шляху"
    path = []
    cur = target
    while cur != -1:
        path.append(str(cur))
        if cur == start:
            break
        cur = pred[cur]
    return " -> ".join(reversed(path))


def floyd_warshall(n: int, edges: List[Tuple[int, int, int]]):
    """Алгоритм Флойда для побудови матриці найкоротших відстаней між усіма парами вершин."""
    INF = float("inf")
    dist = [[0 if i == j else INF for j in range(n)] for i in range(n)]

    for u, v, w in edges:
        dist[u - 1][v - 1] = w
        dist[v - 1][u - 1] = w

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    return dist


if __name__ == "__main__":
    N = 8
    START = 1
    EDGES = [
        (1, 3, 2),
        (1, 4, 4),
        (1, 5, 6),
        (1, 6, 8),
        (3, 4, 3),
        (3, 6, 7),
        (3, 8, 4),
        (2, 5, 6),
        (2, 6, 3),
        (4, 5, 1),
        (5, 7, 4),
        (6, 7, 3),
        (6, 8, 1),
        (7, 8, 5),
    ]

    pred, dist = dijkstra(N, EDGES, start=START)
    print(f"Алгоритм Дейкстри (старт s = {START}):")
    for v in range(1, N + 1):
        print(f"  До вершини {v}: шлях = {reconstruct_path(pred, START, v)}, довжина = {dist[v]}")

    d_matrix = floyd_warshall(N, EDGES)
    print("\nПідсумкова матриця найкоротших відстаней D^(8) за алгоритмом Флойда:")
    header = "     " + " ".join(f"{v:>3}" for v in range(1, N + 1))
    print(header)
    for i, row in enumerate(d_matrix, 1):
        row_str = " ".join("INF" if x == float("inf") else f"{int(x):>3}" for x in row)
        print(f"  {i}: {row_str}")
