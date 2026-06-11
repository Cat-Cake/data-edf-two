import csv


def prepare_clean_csv(input_file="edf_data.csv", output_file="edf_clean.csv"):
    with open(input_file, "r", encoding="utf-8-sig", errors="replace", newline="") as infile, \
         open(output_file, "w", encoding="utf-8", newline="") as outfile:

        reader = csv.reader(infile, delimiter=",", quotechar='"')
        writer = csv.writer(outfile, delimiter=";")

        header = next(reader, None)
        if not header:
            print("Fichier vide")
            return

        # Nouveau format : perimetre_juridique, perimetre_spatial, Status, Identifiant,
        # Numéro de version, Nom, Filière, Date de publication, Date de début, Date de fin,
        # Type, Cause, Information complémentaire, Puissance maximale (MW), Puissance disponible (MW)
        writer.writerow(["nom", "production", "annee", "puissance_max"])

        for row in reader:
            if len(row) < 15:
                continue

            status = row[2].strip()
            if status not in ("Active", "Inactive"):
                continue
            if row[6].strip() != "Nucléaire":
                continue
            if row[10].strip() == "Chronique PMIN":
                continue

            nom = row[5].strip()
            puissance_max = row[13].strip().replace(",", ".")
            production = row[14].strip().replace(",", ".")
            date_debut = row[8].strip()

            if not nom or not production:
                continue

            try:
                production = float(production)
                puissance_max = float(puissance_max) if puissance_max else 0.0
            except ValueError:
                continue

            if production == 0:
                continue

            annee = date_debut[:4] if date_debut else ""

            writer.writerow([nom, production, annee, puissance_max])

    print(f"Fichier nettoyé créé : {output_file}")


if __name__ == "__main__":
    prepare_clean_csv()