def swap(arr, i, j):
    """Міняє місцями два елементи в масиві."""
    arr[i], arr[j] = arr[j], arr[i]


def sink(arr, i, n, stats=None, trace=False):
    """
    Процедура 'занурення' елемента вниз по купі.
    arr: масив
    i: індекс поточного елемента
    n: розмір купи
    """
    k = i
    if stats is not None:
        stats["assignments"] += 1

    while True:
        j = 2 * k + 1
        if stats is not None:
            stats["assignments"] += 1

        if j >= n:
            if trace:
                print(f"Елемент {arr[k]} на індексі {k} досяг кінця купи. Завершуємо.")
            break

        if j + 1 < n:
            if stats is not None:
                stats["comparisons"] += 1
            if arr[j + 1] > arr[j]:
                if trace:
                    print(f"Порівнюємо {arr[j]} (лівий) та {arr[j + 1]} (правий). Обираємо {arr[j + 1]}")
                j += 1
                if stats is not None:
                    stats["assignments"] += 1
            else:
                if trace:
                    print(f"Порівнюємо {arr[j]} (лівий) та {arr[j + 1]} (правий). Обираємо {arr[j]}")
        else:
            if trace:
                print(f"Обираємо лівий дочірній елемент: {arr[j]} на індексі {j}")

        if stats is not None:
            stats["comparisons"] += 1
        if arr[k] >= arr[j]:
            if trace:
                print(f"{arr[k]} (батько) >= {arr[j]} (найбільший дочірній). Елемент на своєму місці.")
            break

        if trace:
            print(f"Міняємо місцями {arr[k]} (батько) та {arr[j]} (дочірній)")
        swap(arr, k, j)
        if stats is not None:
            stats["assignments"] += 3
        if trace:
            print(f"Масив після обміну: {arr}")
        k = j
        if stats is not None:
            stats["assignments"] += 1


def heapsort(arr, trace=False):
    """
    Алгоритм пірамідального сортування (Heapsort).
    """
    n = len(arr)
    stats = {"comparisons": 0, "assignments": 1}
    print(f"Початковий масив: {arr}\n")

    print("--- Фаза 1: Побудова максимальної купи ---")
    for i in range(n // 2 - 1, -1, -1):
        if trace:
            print(f"Починаємо 'занурювати' елемент: {arr[i]} з індексу {i}")
        else:
            print(f"Занурюємо елемент з індексу {i}: {arr[i]}")
        sink(arr, i, n, stats=stats, trace=trace)

    print(f"\nМасив після побудови купи: {arr}\n")

    print("--- Фаза 2: Сортування ---")
    for i in range(n - 1, 0, -1):
        print(f"Міняємо місцями корінь ({arr[0]}) та останній елемент ({arr[i]})")
        swap(arr, 0, i)
        stats["assignments"] += 3

        n -= 1
        stats["assignments"] += 1
        print(f"Розмір купи зменшився до {n}. Відновлюємо властивості купи.")
        if trace:
            print(f"Починаємо 'занурювати' елемент: {arr[0]} з індексу 0")
        sink(arr, 0, n, stats=stats, trace=trace)
        print(f"Масив на поточному кроці: {arr}\n")

    return arr, stats


if __name__ == "__main__":
    variant_15 = [50, 80, 19, 86, 35, 7, 60, 48, 51]

    print("=== ЗАПУСК БАЗОВОЇ РЕАЛІЗАЦІЇ (ТАБЛИЦЯ 3.3) ===")
    arr_basic = variant_15.copy()
    sorted_basic, stats_basic = heapsort(arr_basic, trace=False)
    print(f"Відсортований масив: {sorted_basic}")
    print(f"Кількість порівнянь: {stats_basic['comparisons']}")
    print(f"Кількість присвоювань: {stats_basic['assignments']}\n")

    print("=== ДЕТАЛЬНЕ ТРАСУВАННЯ (ТАБЛИЦЯ 3.4) ===")
    arr_traced = variant_15.copy()
    sorted_traced, _ = heapsort(arr_traced, trace=True)
    print(f"Відсортований масив: {sorted_traced}")
