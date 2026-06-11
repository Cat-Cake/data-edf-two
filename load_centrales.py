import csv


def load_centrales(filename="centrales.csv"):
    centrales = []
    with open(filename, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            gps = row.get("Point gps (wsg84)", "").strip().strip('"')
            lat, lon = None, None
            if gps:
                parts = gps.split(",")
                if len(parts) == 2:
                    try:
                        lat = float(parts[0].strip())
                        lon = float(parts[1].strip())
                    except ValueError:
                        pass

            puissance_installee = row.get("Puissance installée ", "").strip()
            puissance_min = row.get("Puissance minimum de conception", "").strip()
            reserve = row.get("reserve_secondaire_maximale", "").strip()

            centrales.append({
                "tri": int(row["Tri"]) if row.get("Tri") else None,
                "centrale": row.get("Centrale", "").strip(),
                "tranche": row.get("Tranche", "").strip(),
                "filiere": row.get("Filière", "").strip(),
                "combustible": row.get("Combustible", "").strip(),
                "contrat_programme": row.get("Contrat programme", "").strip(),
                "date_mise_en_service": row.get("Date de mise en service industrielle", "").strip() or None,
                "puissance_installee": float(puissance_installee) if puissance_installee else None,
                "puissance_min": float(puissance_min) if puissance_min else None,
                "unite": row.get("Unité", "").strip(),
                "latitude": lat,
                "longitude": lon,
                "region": row.get("Région", "").strip(),
                "departement": row.get("Département", "").strip(),
                "commune": row.get("Commune", "").strip(),
                "sous_filiere": row.get("Sous-filière", "").strip(),
                "reserve_secondaire_maximale": float(reserve) if reserve else None,
            })
    return centrales
