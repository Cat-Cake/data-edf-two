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
        annee = int(parts[2].strip())
        production = float(parts[1].strip())
        puissance_max = float(parts[3].strip())

        if annee != target_year:
            return None

        centrale = extract_centrale(nom)
        indisponibilite = puissance_max - production

        return centrale, indisponibilite

    except ValueError:
        return None


def run_stats_centrale_plus_indis_prod(filename, target_year=2026):
    indis_centrale = defaultdict(float)

    with open(filename, encoding="utf-8") as f:
        for line in f:
            result = mapper(line.strip(), target_year)

            if result is not None:
                centrale, indis = result
                indis_centrale[centrale] += indis

    plus_indis_centrale = max(
        indis_centrale.items(), key=lambda x: x[1]
    )

    return {
        "annee": target_year,
        "plus_indisponibilite": {
            "centrale": plus_indis_centrale[0],
            "indisponibilite": plus_indis_centrale[1]
        }
    }
