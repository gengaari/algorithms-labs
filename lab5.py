from typing import List, Tuple, Dict


def build_representations(n: int, edges: List[Tuple[int, int, int]]):
    """Будує матрицю вагових коефіцієнтів та списки суміжності для графа з вершинами 1..n."""
    INF = float("inf")
    adj_matrix = [[0 if i == j else INF for j in range(n)] for i in range(n)]
    adj_list: Dict[int, List[Tuple[int, int]]] = {i: [] for i in range(1, n + 1)}

    for u, v, w in edges:
        adj_matrix[u - 1][v - 1] = w
        adj_matrix[v - 1][u - 1] = w
        adj_list[u].append((v, w))
        adj_list[v].append((u, w))

    for vertex in adj_list:
        adj_list[vertex].sort(key=lambda item: item[0])

    return adj_matrix, adj_list


def prim_mst(n: int, edges: List[Tuple[int, int, int]], start: int = 1):
    """Алгоритм Пріма для побудови мінімального кістякового дерева."""
    _, adj_list = build_representations(n, edges)
    in_mst = {start}
    mst_edges = []

    while len(in_mst) < n:
        best_edge = None
        for u in sorted(in_mst):
            for v, w in adj_list[u]:
                if v not in in_mst:
                    if best_edge is None or w < best_edge[2]:
                        best_edge = (u, v, w)
        if best_edge is None:
            break
        u, v, w = best_edge
        in_mst.add(v)
        mst_edges.append(best_edge)

    total_weight = sum(w for _, _, w in mst_edges)
    return mst_edges, total_weight


class DSU:
    """Система непересічних множин (Disjoint Set Union) з оптимізацією за рангом."""

    def __init__(self, n: int):
        self.parent = list(range(n + 1))
        self.rank = [0] * (n + 1)

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True


def kruskal_mst(n: int, edges: List[Tuple[int, int, int]]):
    """Алгоритм Крускала для побудови мінімального кістякового дерева."""
    sorted_edges = sorted(edges, key=lambda item: (item[2], item[0], item[1]))
    dsu = DSU(n)
    mst_edges = []

    for u, v, w in sorted_edges:
        if dsu.union(u, v):
            mst_edges.append((u, v, w))
            if len(mst_edges) == n - 1:
                break

    total_weight = sum(w for _, _, w in mst_edges)
    return mst_edges, total_weight


if __name__ == "__main__":
    N = 8
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

    matrix, adj_list = build_representations(N, EDGES)
    print("Матриця вагових коефіцієнтів (1..8):")
    for i, row in enumerate(matrix, 1):
        formatted = ["INF" if x == float("inf") else f"{x:>3}" for x in row]
        print(f"  {i}: " + " ".join(formatted))

    print("
Списки суміжності:")
    for v, neighbors in adj_list.items():
        print(f"  {v}: {neighbors}")

    p_edges, p_weight = prim_mst(N, EDGES, start=1)
    k_edges, k_weight = kruskal_mst(N, EDGES)

    print("
МКД за алгоритмом Пріма:", p_edges, "| Сумарна вага:", p_weight)
    print("МКД за алгоритмом Крускала:", k_edges, "| Сумарна вага:", k_weight)
