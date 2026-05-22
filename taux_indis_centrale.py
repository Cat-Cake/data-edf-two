from collections import defaultdict


def extract_centrale(nom):
    parts = nom.strip().split()

    if len(parts) > 1 and parts[-1].isdigit():
        return " ".join(parts[:-1])

    return nom.strip()


def mapper(line, target_year=2026):
    if line.startswith("nom;"):
        return None

    parts = line.split(";")
    if len(parts) < 4:
        return None

    try:
        nom = parts[0].strip()
        production = float(parts[1].strip())
        puissance_max = float(parts[3].strip())

        centrale = extract_centrale(nom)
        indisponibilite = puissance_max - production

        return centrale, (indisponibilite, puissance_max)

    except ValueError:
        return None


def reducer(key, values):
    total_indispo = 0
    total_puissance_max = 0

    for indisponibilite, puissance_max in values:
        total_indispo += indisponibilite
        total_puissance_max += puissance_max

    taux = (total_indispo / total_puissance_max) * 100 if total_puissance_max else 0

    return key, {
        "total_indispo": total_indispo,
        "total_puissance_max": total_puissance_max,
        "taux": taux,
    }


def run_taux_indis_centrale(filename):
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
