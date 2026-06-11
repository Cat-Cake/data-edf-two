from collections import defaultdict
from centrale_names import normalize_centrale


def mapper(line):
    if line.startswith("nom;"):
        return None

    parts = line.split(";")
    if len(parts) < 2:
        return None

    try:
        nom = parts[0].strip()
        production = float(parts[1].strip())
        centrale = normalize_centrale(nom)
        return centrale, (production, production, production, 1)
    except ValueError:
        return None


def reducer(key, values):
    min_val = float("inf")
    max_val = float("-inf")
    total = 0.0
    count = 0

    for vmin, vmax, vsum, vcount in values:
        min_val = min(min_val, vmin)
        max_val = max(max_val, vmax)
        total += vsum
        count += vcount

    mean = total / count if count else 0

    return key, {
        "min": min_val,
        "max": max_val,
        "mean": mean
    }


def run_stats_centrale(filename):
    # Map
    mapped = defaultdict(list)
    with open(filename, encoding="utf-8") as f:
        for line in f:
            result = mapper(line.strip())
            if result is not None:
                key, value = result
                mapped[key].append(value)

    # Reduce
    results = []
    for key, values in mapped.items():
        results.append(reducer(key, values))

    return results
