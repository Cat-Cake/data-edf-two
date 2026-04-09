import csv


def prepare_clean_csv(input_file="edf_data.csv", output_file="edf_clean.csv"):
    with open(input_file, "r", encoding="latin-1", errors="replace", newline="") as infile, \
         open(output_file, "w", encoding="utf-8", newline="") as outfile:

        reader = csv.reader(infile, delimiter=";", quotechar='"')
        writer = csv.writer(outfile, delimiter=";")

        header = next(reader, None)
        if not header:
            print("Fichier vide")
            return

        # on écrit un fichier simple
        writer.writerow(["nom", "production", "annee"])

        for row in reader:
            if len(row) < 12:
                continue

            # ignorer les lignes inactives et les chroniques PMIN
            if row[0].strip() != "Active":
                continue
            if row[7].strip() == "Chronique PMIN":
                continue

            nom = row[3].strip()
            production = row[11].strip().replace(",", ".")
            date_debut = row[5].strip()

            # ignorer les lignes sans puissance disponible
            if not nom or not production:
                continue

            try:
                production = float(production)
            except ValueError:
                continue

            if production == 0:
                continue

            annee = date_debut[:4] if date_debut else ""

            writer.writerow([nom, production, annee])

    print(f"Fichier nettoyé créé : {output_file}")


if __name__ == "__main__":
    prepare_clean_csv()