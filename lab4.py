import math
import re

UKR_POSITIONS = {
    'А': 1, 'Б': 2, 'В': 3, 'Г': 4, 'Ґ': 5, 'Д': 6, 'Е': 7, 'Є': 8, 'Ж': 9, 'З': 10,
    'И': 11, 'І': 12, 'Ї': 13, 'Й': 14, 'К': 15, 'Л': 16, 'М': 17, 'Н': 18, 'О': 19,
    'П': 20, 'Р': 21, 'С': 22, 'Т': 23, 'У': 24, 'Ф': 25, 'Х': 26, 'Ц': 27, 'Ч': 28,
    'Ш': 29, 'Щ': 30, 'Ь': 31, 'Ю': 32, 'Я': 33
}

A_KNUTH = (math.sqrt(5) - 1) / 2
DELETED = "<DELETED>"


def word_to_key(word: str) -> int:
    """Обчислює числовий ключ слова як суму позицій його літер в українському алфавіті."""
    return sum(UKR_POSITIONS.get(ch, 0) for ch in word.upper())


def hash_division(key: int, m: int = 13) -> int:
    """Хеш-функція методом ділення: h(k) = k mod m."""
    return key % m


def hash_multiplication(key: int, m: int = 16, a: float = A_KNUTH) -> int:
    """Хеш-функція методом множення: h(k) = floor(m * (k * A mod 1))."""
    frac_part = (key * a) - math.floor(key * a)
    return math.floor(m * frac_part)


def build_open_hash_table(words: list, m: int, hash_fn) -> list:
    table = [[] for _ in range(m)]
    for word in words:
        k = word_to_key(word)
        addr = hash_fn(k, m)
        table[addr].append(word)
    return table


def search_open_hash_table(table: list, word: str, hash_fn) -> tuple:
    m = len(table)
    addr = hash_fn(word_to_key(word), m)
    comparisons = 0
    for idx, item in enumerate(table[addr]):
        comparisons += 1
        if item == word:
            return addr, idx, comparisons
    return addr, -1, comparisons


def delete_open_hash_table(table: list, word: str, hash_fn) -> tuple:
    addr, pos, comparisons = search_open_hash_table(table, word, hash_fn)
    if pos != -1:
        table[addr].pop(pos)
        return True, comparisons
    return False, comparisons


def display_open_table(table: list, title: str):
    print(f"\n--- {title} ---")
    for i, chain in enumerate(table):
        print(f"Індекс {i:02d}: {chain}")



def build_closed_hash_table(words: list, m: int, hash_fn) -> list:
    table = [None] * m
    for word in words:
        start_addr = hash_fn(word_to_key(word), m)
        for i in range(m):
            addr = (start_addr + i) % m
            if table[addr] is None or table[addr] == DELETED:
                table[addr] = word
                break
        else:
            raise OverflowError(f"Таблиця заповнена. Не вдалося додати слово: {word}")
    return table


def search_closed_hash_table(table: list, word: str, hash_fn) -> tuple:
    m = len(table)
    start_addr = hash_fn(word_to_key(word), m)
    comparisons = 0
    for i in range(m):
        addr = (start_addr + i) % m
        slot = table[addr]
        if slot is None:
            return -1, comparisons
        if slot != DELETED:
            comparisons += 1
            if slot == word:
                return addr, comparisons
    return -1, comparisons


def delete_closed_hash_table(table: list, word: str, hash_fn) -> tuple:
    addr, comparisons = search_closed_hash_table(table, word, hash_fn)
    if addr != -1:
        table[addr] = DELETED
        return True, comparisons
    return False, comparisons


def display_closed_table(table: list, title: str):
    print(f"\n--- {title} ---")
    for i, item in enumerate(table):
        val = item if item is not None else "(NULL)"
        print(f"Індекс {i:02d} | {val}")


if __name__ == "__main__":
    SENTENCE = "Хто грошима величається, той без душі зостачається."
    WORDS = re.findall(r"[А-ЯҐЄІЇ]+", SENTENCE.upper())

    print("Слова варіанта № 15:", WORDS)
    for w in WORDS:
        k = word_to_key(w)
        print(f"{w:<14} -> k = {k:<3} | h_div(13) = {hash_division(k, 13):<2} | h_mul(16) = {hash_multiplication(k, 16):<2}")

    open_div = build_open_hash_table(WORDS, 13, hash_division)
    open_mul = build_open_hash_table(WORDS, 16, hash_multiplication)
    display_open_table(open_div, "Відкрита хеш-таблиця (ділення, M=13)")
    display_open_table(open_mul, "Відкрита хеш-таблиця (множення, M=16)")

    closed_div = build_closed_hash_table(WORDS, 13, hash_division)
    closed_mul = build_closed_hash_table(WORDS, 16, hash_multiplication)
    display_closed_table(closed_div, "Закрита хеш-таблиця (ділення, M=13)")
    display_closed_table(closed_mul, "Закрита хеш-таблиця (множення, M=16)")

    print("\n--- Аналіз порівнянь при пошуку/видаленні ---")
    for name, tbl, search_fn, h_fn in [
        ("Відкрита (ділення, M=13)", open_div, search_open_hash_table, hash_division),
        ("Відкрита (множення, M=16)", open_mul, search_open_hash_table, hash_multiplication),
        ("Закрита (ділення, M=13)", closed_div, search_closed_hash_table, hash_division),
        ("Закрита (множення, M=16)", closed_mul, search_closed_hash_table, hash_multiplication),
    ]:
        comps = [search_fn(tbl, w, h_fn)[-1] for w in WORDS]
        max_c = max(comps)
        max_words = [w for w, c in zip(WORDS, comps) if c == max_c]
        print(f"{name}: сума = {sum(comps)}, середня = {sum(comps)/len(WORDS):.2f}, макс = {max_c} ({', '.join(max_words)})")
