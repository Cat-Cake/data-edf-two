from collections import defaultdict


def mapper(line):
    if line.startswith("annee;"):
        return None

    parts = line.split(";")
    if len(parts) < 2:
        return None

    try:
        annee = parts[0].strip()
        production = float(parts[1].strip())
        if not annee:
            return None
        return annee, production
    except ValueError:
        return None


def reducer(key, values):
    total = sum(values)
    return key, {"production_gwh": total}


def run_prod_hist_annee(filename):
    mapped = defaultdict(list)
    with open(filename, encoding="utf-8") as f:
        for line in f:
            result = mapper(line.strip())
            if result is not None:
                key, value = result
                mapped[key].append(value)

    results = []
    for key, values in mapped.items():
        results.append(reducer(key, values))

    results.sort(key=lambda x: x[0])
    return results
