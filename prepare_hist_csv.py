import csv


def prepare_hist_csv(input_file="edf_hist.csv", output_file="edf_hist_clean.csv"):
    with open(input_file, "r", encoding="utf-8-sig", errors="replace", newline="") as infile, \
         open(output_file, "w", encoding="utf-8", newline="") as outfile:

        reader = csv.DictReader(infile, delimiter=",")
        writer = csv.writer(outfile, delimiter=";")
        writer.writerow(["annee", "production_gwh"])

        for row in reader:
            annee = row.get("Année", "").strip()
            filiere = row.get("Filiere", "").strip()
            production = row.get("Energie produite", "").strip().replace(",", ".")

            if filiere != "Nucléaire":
                continue
            if not annee or not production:
                continue

            try:
                production = float(production)
            except ValueError:
                continue

            writer.writerow([annee, production])

    print(f"Fichier historique nettoyé créé : {output_file}")


if __name__ == "__main__":
    prepare_hist_csv()
