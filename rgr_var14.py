import heapq
import random
import time
import matplotlib.pyplot as plt


def dijkstra_single_source(n: int, adj: dict, start: int):
    """Пошук найкоротших шляхів від стартової вершини start в орієнтованому графі."""
    INF = float("inf")
    dist = [INF] * n
    pred = [-1] * n
    dist[start] = 0
    visited = [False] * n
    pq = [(0, start)]

    while pq:
        d_u, u = heapq.heappop(pq)
        if visited[u]:
            continue
        visited[u] = True
        for v, w in adj[u]:
            if not visited[v] and d_u + w < dist[v]:
                dist[v] = d_u + w
                pred[v] = u
                heapq.heappush(pq, (dist[v], v))
    return dist, pred


def all_pairs_dijkstra(n: int, edges: list):
    """N-разовий виклик алгоритму Дейкстри для пошуку шляхів між усіма парами вершин."""
    adj = {i: [] for i in range(n)}
    for u, v, w in edges:
        adj[u].append((v, w))

    dist_matrix = []
    pred_matrix = []
    for s in range(n):
        d, p = dijkstra_single_source(n, adj, s)
        dist_matrix.append(d)
        pred_matrix.append(p)
    return dist_matrix, pred_matrix


def floyd_warshall(n: int, edges: list):
    """Алгоритм Флойда-Воршелла для пошуку найкоротших шляхів між усіма парами вершин."""
    INF = float("inf")
    dist = [[0 if i == j else INF for j in range(n)] for i in range(n)]
    next_node = [[None for _ in range(n)] for _ in range(n)]

    for u, v, w in edges:
        if w < dist[u][v]:
            dist[u][v] = w
            next_node[u][v] = v

    for k in range(n):
        dist_k = dist[k]
        for i in range(n):
            dik = dist[i][k]
            if dik == INF:
                continue
            dist_i = dist[i]
            next_i = next_node[i]
            for j in range(n):
                if dist_k[j] != INF and dik + dist_k[j] < dist_i[j]:
                    dist_i[j] = dik + dist_k[j]
                    next_i[j] = next_i[k]
    return dist, next_node


def reconstruct_path_floyd(next_node: list, u: int, v: int):
    """Відновлення найкоротшого маршруту від вершини u до v (1-індексація у виводі)."""
    if u == v:
        return [u + 1]
    if next_node[u][v] is None:
        return []
    path = [u + 1]
    cur = u
    while cur != v:
        cur = next_node[cur][v]
        if cur is None:
            return []
        path.append(cur + 1)
    return path


def generate_directed_graph(n: int, density_mode: str, seed: int = 14):
    """Генератор зважених орієнтованих графів: 'sparse' (|E| ~ 3n) або 'dense' (|E| ~ 0.75n^2)."""
    rng = random.Random(seed + n)
    edges = [(i, (i + 1) % n, rng.randint(1, 20)) for i in range(n)]
    existing = {(u, v) for u, v, _ in edges}

    if density_mode == "sparse":
        target_edges = 3 * n
        while len(edges) < target_edges:
            u = rng.randrange(n)
            v = rng.randrange(n)
            if u != v and (u, v) not in existing:
                existing.add((u, v))
                edges.append((u, v, rng.randint(1, 50)))
    else:
        for u in range(n):
            for v in range(n):
                if u != v and (u, v) not in existing and rng.random() < 0.75:
                    existing.add((u, v))
                    edges.append((u, v, rng.randint(1, 50)))
    return edges


if __name__ == "__main__":
    # 1. Контрольний приклад (5 вершин, 10 орієнтованих ребер)
    ctrl_n = 5
    ctrl_edges_1based = [
        (1, 2, 4), (1, 3, 2), (2, 3, 1), (2, 4, 5), (3, 2, 1),
        (3, 4, 8), (3, 5, 10), (4, 5, 2), (5, 1, 3), (5, 4, 6),
    ]
    ctrl_edges = [(u - 1, v - 1, w) for u, v, w in ctrl_edges_1based]

    dijk_mat, _ = all_pairs_dijkstra(ctrl_n, ctrl_edges)
    floyd_mat, floyd_next = floyd_warshall(ctrl_n, ctrl_edges)
    assert dijk_mat == floyd_mat, "Помилка: матриці не збігаються!"

    print("=== Контрольний орієнтований граф (n = 5, m = 10) ===")
    print("Перевірка збігу матриць Дейкстри та Флойда: OK (повний збіг)")
    print("Підсумкова матриця найкоротших відстаней D:")
    for idx, row in enumerate(floyd_mat, 1):
        print(f"  {idx}: {row}")

    p_1_5 = " -> ".join(map(str, reconstruct_path_floyd(floyd_next, 0, 4)))
    p_4_2 = " -> ".join(map(str, reconstruct_path_floyd(floyd_next, 3, 1)))
    print(f"Приклад відновлення маршруту 1 -> 5: {p_1_5} (вага = {floyd_mat[0][4]})")
    print(f"Приклад відновлення маршруту 4 -> 2: {p_4_2} (вага = {floyd_mat[3][1]})")

    # 2. Експериментальне порівняння на розріджених та щільних орграфах
    sizes = [50, 100, 150, 200, 300, 400]
    d_sp_times, f_sp_times = [], []
    d_dn_times, f_dn_times = [], []

    print("\n=== Порівняння швидкодії (мс) ===")
    for n_val in sizes:
        sp_edges = generate_directed_graph(n_val, "sparse")
        t0 = time.perf_counter()
        d_sp, _ = all_pairs_dijkstra(n_val, sp_edges)
        t_d_sp = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        f_sp, _ = floyd_warshall(n_val, sp_edges)
        t_f_sp = (time.perf_counter() - t0) * 1000
        assert d_sp == f_sp

        dn_edges = generate_directed_graph(n_val, "dense")
        t0 = time.perf_counter()
        d_dn, _ = all_pairs_dijkstra(n_val, dn_edges)
        t_d_dn = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        f_dn, _ = floyd_warshall(n_val, dn_edges)
        t_f_dn = (time.perf_counter() - t0) * 1000
        assert d_dn == f_dn

        d_sp_times.append(t_d_sp)
        f_sp_times.append(t_f_sp)
        d_dn_times.append(t_d_dn)
        f_dn_times.append(t_f_dn)

        print(f"|V|={n_val:>3} | розрідж. (|E|={len(sp_edges):>4}): Дейкстра={t_d_sp:6.2f} мс, Флойд={t_f_sp:6.2f} мс | "
              f"щільн. (|E|={len(dn_edges):>6}): Дейкстра={t_d_dn:6.2f} мс, Флойд={t_f_dn:6.2f} мс")

    # 3. Побудова графіків порівняння швидкодії
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8))
    ax1.plot(sizes, d_sp_times, marker="o", label="|V|-разовий Дейкстра")
    ax1.plot(sizes, f_sp_times, marker="s", label="Флойд–Воршелл")
    ax1.set_title("Розріджені орієнтовані графи (|E| ≈ 3|V|)")
    ax1.set_xlabel("Кількість вершин |V|")
    ax1.set_ylabel("Час виконання, мс")
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.legend()

    ax2.plot(sizes, d_dn_times, marker="o", label="|V|-разовий Дейкстра")
    ax2.plot(sizes, f_dn_times, marker="s", label="Флойд–Воршелл")
    ax2.set_title("Щільні орієнтовані графи (|E| ≈ 0.75|V|²)")
    ax2.set_xlabel("Кількість вершин |V|")
    ax2.set_ylabel("Час виконання, мс")
    ax2.grid(True, linestyle="--", alpha=0.5)
    ax2.legend()

    plt.tight_layout()
    plt.savefig("rgr_var14_benchmark.png", dpi=200)
    plt.show()
