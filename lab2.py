"""
Лабораторна робота № 2
Логарифмічні алгоритми сортування
Студент: Фам Чам Ян, група АІ-252, Варіант № 15
Послідовність: [50, 80, 19, 86, 35, 7, 60, 48, 51]
"""


# 1. Ітеративна реалізація сортування злиттям (Лістинг 2.1)
def merge_sort_iterative(a, trace=False):
    n = len(a)
    comparisons = 0
    assignments = 0
    if trace:
        print(f"Початковий масив: {a}")

    i = 1
    assignments += 1
    while i < n:
        j = 0
        assignments += 1
        while j < n - i:
            left = j
            mid = j + i
            right = min(j + 2 * i, n)
            assignments += 3
            if trace:
                print(
                    f"Об'єднуємо підмасиви: a[{left}:{mid}] ({a[left:mid]}) "
                    f"і a[{mid}:{right}] ({a[mid:right]})"
                )

            c, a_count = merge_iterative(a, left, mid, right, trace=trace)
            comparisons += c
            assignments += a_count
            if trace:
                print(f"Масив після об'єднання: {a}")

            j += 2 * i
            assignments += 1
        i *= 2
        assignments += 1

    return a, comparisons, assignments


def merge_iterative(a, left, mid, right, trace=False):
    comparisons = 0
    assignments = 0
    n1 = mid - left
    n2 = right - mid
    L = a[left:mid]
    R = a[mid:right]
    assignments += n1 + n2

    it1 = 0
    it2 = 0
    k = left
    assignments += 3

    while it1 < n1 and it2 < n2:
        comparisons += 1
        if L[it1] < R[it2]:
            if trace:
                print(f"  Порівняння: {L[it1]} < {R[it2]} -> True")
            a[k] = L[it1]
            it1 += 1
            assignments += 2
        else:
            if trace:
                print(f"  Порівняння: {L[it1]} < {R[it2]} -> False")
            assignments += 1
            a[k] = R[it2]
            it2 += 1
            assignments += 2
        k += 1
        assignments += 1

    while it1 < n1:
        a[k] = L[it1]
        if trace:
            print(f"  Додаємо залишок з лівого масиву: {L[it1]}")
        it1 += 1
        k += 1
        assignments += 3

    while it2 < n2:
        a[k] = R[it2]
        if trace:
            print(f"  Додаємо залишок з правого масиву: {R[it2]}")
        it2 += 1
        k += 1
        assignments += 3

    return comparisons, assignments


# 2. Рекурсивна реалізація сортування злиттям (Лістинг 2.2)
def merge_sort_recursive(arr, trace=False, depth=0):
    comparisons = 0
    assignments = 0
    recursive_calls = 0
    indent = "  " * depth

    if trace:
        print(f"{indent}Розділяємо масив: {arr}")

    if len(arr) <= 1:
        return arr, comparisons, assignments, recursive_calls

    mid = len(arr) // 2
    assignments += 1
    recursive_calls += 2

    left_half, c1, a1, r1 = merge_sort_recursive(arr[:mid], trace=trace, depth=depth + 1)
    right_half, c2, a2, r2 = merge_sort_recursive(arr[mid:], trace=trace, depth=depth + 1)

    comparisons += c1 + c2
    assignments += a1 + a2
    recursive_calls += r1 + r2

    merged_arr, c_merge, a_merge = merge_recursive(left_half, right_half, trace=trace, indent=indent)
    comparisons += c_merge
    assignments += a_merge

    return merged_arr, comparisons, assignments, recursive_calls


def merge_recursive(left, right, trace=False, indent=""):
    merged_arr = []
    comparisons = 0
    assignments = 0
    i = 0
    j = 0
    assignments += 2

    if trace:
        print(f"{indent}Зливаємо {left} та {right}")

    while i < len(left) and j < len(right):
        comparisons += 1
        if left[i] <= right[j]:
            if trace:
                print(f"{indent}  Порівняння: {left[i]} <= {right[j]} -> True. Додаємо {left[i]}")
            merged_arr.append(left[i])
            i += 1
            assignments += 2
        else:
            if trace:
                print(f"{indent}  Порівняння: {left[i]} <= {right[j]} -> False. Додаємо {right[j]}")
            merged_arr.append(right[j])
            j += 1
            assignments += 2

    while i < len(left):
        if trace:
            print(f"{indent}  Додаємо залишок з лівого масиву: {left[i]}")
        merged_arr.append(left[i])
        i += 1
        assignments += 2

    while j < len(right):
        if trace:
            print(f"{indent}  Додаємо залишок з правого масиву: {right[j]}")
        merged_arr.append(right[j])
        j += 1
        assignments += 2

    if trace:
        print(f"{indent}Злиття завершено. Результат: {merged_arr}")

    return merged_arr, comparisons, assignments


# 3. Швидке сортування за схемою Хоара (Лістинг 2.3)
def quicksort(a, l, r, trace=False, depth=0):
    comparisons = 0
    assignments = 0
    recursive_calls = 1
    indent = "  " * depth

    if trace:
        print(f"{indent}Quicksort виклик: масив = {a[l:r+1]}, l={l}, r={r}")

    if l < r:
        q, c1, a1 = partition(a, l, r, trace=trace, indent=indent)
        comparisons += c1
        assignments += a1

        c2, a2, r2 = quicksort(a, l, q, trace=trace, depth=depth + 1)
        c3, a3, r3 = quicksort(a, q + 1, r, trace=trace, depth=depth + 1)

        comparisons += c2 + c3
        assignments += a2 + a3
        recursive_calls += r2 + r3

        if trace:
            print(f"{indent}Після Quicksort для l={l}, r={r}: масив = {a}")
        return comparisons, assignments, recursive_calls
    else:
        return 0, 0, recursive_calls


def partition(a, l, r, trace=False, indent=""):
    comparisons = 0
    assignments = 0

    pivot = a[l]
    assignments += 1
    if trace:
        print(f"{indent}  Вибираємо опорний елемент (pivot): {pivot}")

    i = l - 1
    j = r + 1
    assignments += 2

    while True:
        i += 1
        assignments += 1
        while a[i] < pivot:
            comparisons += 1
            i += 1
            assignments += 1
        comparisons += 1

        j -= 1
        assignments += 1
        while a[j] > pivot:
            comparisons += 1
            j -= 1
            assignments += 1
        comparisons += 1

        comparisons += 1
        if i >= j:
            if trace:
                print(
                    f"{indent}  Поточні індекси: i={i}, j={j}. "
                    f"Індекси перетнулися. Поділ завершено. Повертаємо j={j}. Масив: {a}"
                )
            return j, comparisons, assignments

        if trace:
            print(f"{indent}  Поточні індекси: i={i}, j={j}. Обмінюємо a[{i}] ({a[i]}) і a[{j}] ({a[j]})")
        a[i], a[j] = a[j], a[i]
        assignments += 3


if __name__ == "__main__":
    variant_15 = [50, 80, 19, 86, 35, 7, 60, 48, 51]

    print("=" * 60)
    print("1. ІТЕРАТИВНЕ СОРТУВАННЯ ЗЛИТТЯМ (MERGE SORT ITERATIVE)")
    print("=" * 60)
    res_iter, c_iter, a_iter = merge_sort_iterative(variant_15.copy(), trace=True)
    print("Відсортований список:", res_iter)
    print(f"Кількість порівнянь: {c_iter}")
    print(f"Кількість присвоювань: {a_iter}\n")

    print("=" * 60)
    print("2. РЕКУРСИВНЕ СОРТУВАННЯ ЗЛИТТЯМ (MERGE SORT RECURSIVE)")
    print("=" * 60)
    res_rec, c_rec, a_rec, r_rec = merge_sort_recursive(variant_15.copy(), trace=True)
    print("Відсортований список:", res_rec)
    print(f"Загальна кількість порівнянь: {c_rec}")
    print(f"Загальна кількість присвоювань: {a_rec}")
    print(f"Загальна кількість рекурсивних викликів: {r_rec}\n")

    print("=" * 60)
    print("3. ШВИДКЕ СОРТУВАННЯ ЗА СХЕМОЮ ХОАРА (QUICKSORT HOARE)")
    print("=" * 60)
    qs_list = variant_15.copy()
    c_qs, a_qs, r_qs = quicksort(qs_list, 0, len(qs_list) - 1, trace=True)
    print("Відсортований список:", qs_list)
    print(f"Загальна кількість порівнянь: {c_qs}")
    print(f"Загальна кількість присвоювань: {a_qs}")
    print(f"Загальна кількість рекурсивних викликів: {r_qs}")
