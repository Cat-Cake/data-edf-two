from collections import defaultdict


def mapper(line):
    if line.startswith("nom;"):
        return None

    parts = line.split(";")
    if len(parts) < 3:
        return None

    try:
        nom = parts[0].strip()
        production = float(parts[1].strip())
        annee = parts[2].strip()
        if not annee:
            return None
        centrale = nom.rsplit(" ", 1)[0]
        return (centrale, annee), production
    except ValueError:
        return None


def reducer(key, values):
    total = sum(values)
    centrale, annee = key
    return key, {"centrale": centrale, "annee": annee, "total_production": total}


def run_prod_centrale_annee(filename):
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
