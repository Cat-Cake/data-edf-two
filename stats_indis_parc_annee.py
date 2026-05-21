from collections import defaultdict


def mapper(line):
    if line.startswith("nom;"):
        return None

    parts = line.split(";")
    if len(parts) < 4:
        return None

    try:
        annee = parts[2].strip()
        puissance_max = float(parts[3].strip())
        production = float(parts[1].strip())
        if not annee:
            return None
        indisponibilite = puissance_max - production
        return annee, indisponibilite
    except ValueError:
        return None


def reducer(key, values):
    total = sum(values)
    return key, {"total_indisponibilite": total}


def run_indis_parc_annee(filename):
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
