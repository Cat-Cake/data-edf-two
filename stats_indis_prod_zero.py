import csv
from collections import defaultdict


def mapper(row):
    # ignorer les lignes inactives et les chroniques PMIN
    if row[0].strip() != "Active":
        return None
    if row[7].strip() == "Chronique PMIN":
        return None

    try:
        puissance_disponible = row[11].strip().replace(",", ".")
        puissance_max = row[10].strip().replace(",", ".")

        if not puissance_disponible or not puissance_max:
            return None

        puissance_disponible = float(puissance_disponible)
        puissance_max = float(puissance_max)

        if puissance_disponible != 0:
            return None

        return "PARC", puissance_max
    except ValueError:
        return None


def reducer(key, values):
    total = sum(values)
    return key, {"total_indisponibilite_prod_zero": total}


def run_indis_prod_zero(filename):
    # Map
    mapped = defaultdict(list)
    with open(filename, encoding="latin-1", errors="replace", newline="") as f:
        reader = csv.reader(f, delimiter=";", quotechar='"')
        next(reader, None)  # skip header
        for row in reader:
            if len(row) < 12:
                continue
            result = mapper(row)
            if result is not None:
                key, value = result
                mapped[key].append(value)

    # Reduce
    results = []
    for key, values in mapped.items():
        results.append(reducer(key, values))

    return results
