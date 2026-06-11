import csv
from collections import defaultdict


def mapper(row):
    if row[2].strip() not in ("Active", "Inactive"):
        return None
    if row[6].strip() != "Nucléaire":
        return None
    if row[10].strip() == "Chronique PMIN":
        return None
    return "PARC", 1


def reducer(key, values):
    return key, {"nb_periodes": sum(values)}


def run_nb_indis_parc(filename):
    mapped = defaultdict(list)
    with open(filename, encoding="utf-8-sig", errors="replace", newline="") as f:
        reader = csv.reader(f, delimiter=",")
        next(reader, None)
        for row in reader:
            if len(row) < 15:
                continue
            result = mapper(row)
            if result is not None:
                key, value = result
                mapped[key].append(value)

    return [reducer(key, values) for key, values in mapped.items()]
