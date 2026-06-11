from collections import defaultdict
from centrale_names import normalize_centrale


def mapper(line, target_year=2026):
    if line.startswith("nom;"):
        return None

    parts = line.split(";")
    if len(parts) < 4:
        return None

    try:
        nom = parts[0].strip()
        production = float(parts[1].strip())
        annee = int(parts[2].strip())

        if annee != target_year:
            return None

        centrale = normalize_centrale(nom)

        return centrale, production

    except ValueError:
        return None


def run_stats_centrale_meilleur_prod(filename, target_year=2026):
    production_centrale = defaultdict(float)

    with open(filename, encoding="utf-8") as f:
        for line in f:
            result = mapper(line.strip(), target_year)

            if result is not None:
                centrale, production = result
                production_centrale[centrale] += production

    meilleur_centrale = max(
        production_centrale.items(), key=lambda x: x[1]
    )

    return {
        "annee": target_year,
        "meilleur_production": {
            "centrale": meilleur_centrale[0],
            "production": meilleur_centrale[1]
        }
    }
