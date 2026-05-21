from collections import defaultdict


def mapper(line):
    if line.startswith("nom;"):
        return None

    parts = line.split(";")
    if len(parts) < 4:
        return None

    try:
        production = float(parts[1].strip())
        puissance_max = float(parts[3].strip())
        indisponibilite = puissance_max - production
        return "PARC", indisponibilite
    except ValueError:
        return None


def reducer(key, values):
    total = sum(values)
    return key, {"total_indisponibilite_prod_sup_zero": total}


def run_indis_prod_sup_zero(filename):
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
