import psycopg2
import os

from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}


def get_connection():
    print('Connecting to PostgreSQL...')
    conn = psycopg2.connect(**DB_CONFIG)
    return conn


def create_tables(conn):
    print('Creating tables...')
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS stats_parc (
                id SERIAL PRIMARY KEY,
                min FLOAT NOT NULL,
                max FLOAT NOT NULL,
                mean FLOAT NOT NULL
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS stats_centrale (
                id SERIAL PRIMARY KEY,
                centrale VARCHAR(255) NOT NULL,
                min FLOAT NOT NULL,
                max FLOAT NOT NULL,
                mean FLOAT NOT NULL
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS stats_centrale_tranche (
                id SERIAL PRIMARY KEY,
                tranche VARCHAR(255) NOT NULL,
                min FLOAT NOT NULL,
                max FLOAT NOT NULL,
                mean FLOAT NOT NULL
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS prod_parc_annee (
                id SERIAL PRIMARY KEY,
                annee VARCHAR(10) NOT NULL,
                total_production FLOAT NOT NULL
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS prod_centrale_annee (
                id SERIAL PRIMARY KEY,
                centrale VARCHAR(255) NOT NULL,
                annee VARCHAR(10) NOT NULL,
                total_production FLOAT NOT NULL
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS indis_parc_annee (
                id SERIAL PRIMARY KEY,
                annee VARCHAR(10) NOT NULL,
                total_indisponibilite FLOAT NOT NULL
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS indis_prod_zero (
                id SERIAL PRIMARY KEY,
                total_indisponibilite_prod_zero FLOAT NOT NULL
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS indis_prod_sup_zero (
                id SERIAL PRIMARY KEY,
                total_indisponibilite_prod_sup_zero FLOAT NOT NULL
            );
        """)
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS centrale_meilleur_prod (
                        id SERIAL PRIMARY KEY,
                        centrale VARCHAR(255) NOT NULL,
                        annee VARCHAR(10) NOT NULL,
                        production FLOAT NOT NULL
                    );
                """)
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS centrale_moins_bonne_prod (
                        id SERIAL PRIMARY KEY,
                        centrale VARCHAR(255) NOT NULL,
                        annee VARCHAR(10) NOT NULL,
                        production FLOAT NOT NULL
                    );
                """)
        cur.execute("""
                        CREATE TABLE IF NOT EXISTS centrale_plus_indisponibilite (
                            id SERIAL PRIMARY KEY,
                            centrale VARCHAR(255) NOT NULL,
                            annee VARCHAR(10) NOT NULL,
                            indisponibilite FLOAT NOT NULL
                        );
                    """)
        cur.execute("""
                        CREATE TABLE IF NOT EXISTS centrale_moins_indisponibilite (
                            id SERIAL PRIMARY KEY,
                            centrale VARCHAR(255) NOT NULL,
                            annee VARCHAR(10) NOT NULL,
                            indisponibilite FLOAT NOT NULL
                        );
                    """)
        cur.execute("""
                        CREATE TABLE IF NOT EXISTS taux_indisponibilite_parc (
                            id SERIAL PRIMARY KEY,
                            taux FLOAT NOT NULL
                        );
                    """)
        cur.execute("""
                        CREATE TABLE IF NOT EXISTS taux_indisponibilite_centrale (
                            id SERIAL PRIMARY KEY,
                            centrale VARCHAR(255) NOT NULL,
                            taux FLOAT NOT NULL
                        );
                    """)
        cur.execute("""
                        CREATE TABLE IF NOT EXISTS taux_indisponibilite_tranche (
                            id SERIAL PRIMARY KEY,
                            tranche VARCHAR(255) NOT NULL,
                            taux FLOAT NOT NULL
                        );
                    """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS centrales (
                id SERIAL PRIMARY KEY,
                tri INT,
                centrale VARCHAR(255) NOT NULL,
                tranche VARCHAR(255) NOT NULL,
                filiere VARCHAR(255),
                combustible VARCHAR(255),
                contrat_programme VARCHAR(50),
                date_mise_en_service DATE,
                puissance_installee FLOAT,
                puissance_min FLOAT,
                unite VARCHAR(20),
                latitude FLOAT,
                longitude FLOAT,
                region VARCHAR(255),
                departement VARCHAR(255),
                commune VARCHAR(255),
                sous_filiere VARCHAR(255),
                reserve_secondaire_maximale FLOAT
            );
        """)
    conn.commit()


def insert_stats_parc(conn, results):
    with conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE stats_parc RESTART IDENTITY;")
        for _, value in results:
            cur.execute(
                "INSERT INTO stats_parc (min, max, mean) VALUES (%s, %s, %s);",
                (value["min"], value["max"], value["mean"])
            )
    conn.commit()


def insert_stats_centrale(conn, results):
    with conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE stats_centrale RESTART IDENTITY;")
        for key, value in results:
            cur.execute(
                "INSERT INTO stats_centrale (centrale, min, max, mean) VALUES (%s, %s, %s, %s);",
                (key, value["min"], value["max"], value["mean"])
            )
    conn.commit()


def insert_stats_centrale_tranche(conn, results):
    with conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE stats_centrale_tranche RESTART IDENTITY;")
        for key, value in results:
            cur.execute(
                "INSERT INTO stats_centrale_tranche (tranche, min, max, mean) VALUES (%s, %s, %s, %s);",
                (key, value["min"], value["max"], value["mean"])
            )
    conn.commit()


def insert_prod_parc_annee(conn, results):
    with conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE prod_parc_annee RESTART IDENTITY;")
        for key, value in results:
            cur.execute(
                "INSERT INTO prod_parc_annee (annee, total_production) VALUES (%s, %s);",
                (key, value["total_production"])
            )
    conn.commit()


def insert_prod_centrale_annee(conn, results):
    with conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE prod_centrale_annee RESTART IDENTITY;")
        for _, value in results:
            cur.execute(
                "INSERT INTO prod_centrale_annee (centrale, annee, total_production) VALUES (%s, %s, %s);",
                (value["centrale"], value["annee"], value["total_production"])
            )
    conn.commit()


def insert_indis_parc_annee(conn, results):
    with conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE indis_parc_annee RESTART IDENTITY;")
        for key, value in results:
            cur.execute(
                "INSERT INTO indis_parc_annee (annee, total_indisponibilite) VALUES (%s, %s);",
                (key, value["total_indisponibilite"])
            )
    conn.commit()


def insert_indis_prod_zero(conn, results):
    with conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE indis_prod_zero RESTART IDENTITY;")
        for _, value in results:
            cur.execute(
                "INSERT INTO indis_prod_zero (total_indisponibilite_prod_zero) VALUES (%s);",
                (value["total_indisponibilite_prod_zero"],)
            )
    conn.commit()


def insert_indis_prod_sup_zero(conn, results):
    with conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE indis_prod_sup_zero RESTART IDENTITY;")
        for _, value in results:
            cur.execute(
                "INSERT INTO indis_prod_sup_zero (total_indisponibilite_prod_sup_zero) VALUES (%s);",
                (value["total_indisponibilite_prod_sup_zero"],)
            )
    conn.commit()


def insert_meilleure_production(conn, result):
    with conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE centrale_meilleur_prod RESTART IDENTITY;")
        sql = """
        INSERT INTO centrale_meilleur_prod (
            annee,
            centrale,
            production
        )
        VALUES (%s, %s, %s)
        """
        cur.execute(sql, (
            result["annee"],
            result["meilleur_production"]["centrale"],
            result["meilleur_production"]["production"]
        ))
    conn.commit()


def insert_moins_bonne_production(conn, result):
    with conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE centrale_moins_bonne_prod RESTART IDENTITY;")
        sql = """
        INSERT INTO centrale_moins_bonne_prod (
            annee,
            centrale,
            production
        )
        VALUES (%s, %s, %s)
        """
        cur.execute(sql, (
            result["annee"],
            result["moins_bonne_production"]["centrale"],
            result["moins_bonne_production"]["production"]
        ))
    conn.commit()


def insert_plus_indisponibilite(conn, result):
    with conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE centrale_plus_indisponibilite RESTART IDENTITY;")
        sql = """
        INSERT INTO centrale_plus_indisponibilite (
            annee,
            centrale,
            indisponibilite
        )
        VALUES (%s, %s, %s)
        """
        cur.execute(sql, (
            result["annee"],
            result["plus_indisponibilite"]["centrale"],
            result["plus_indisponibilite"]["indisponibilite"]
        ))
    conn.commit()


def insert_moins_indisponibilite(conn, result):
    with conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE centrale_moins_indisponibilite RESTART IDENTITY;")
        sql = """
        INSERT INTO centrale_moins_indisponibilite (
            annee,
            centrale,
            indisponibilite
        )
        VALUES (%s, %s, %s)
        """
        cur.execute(sql, (
            result["annee"],
            result["moins_indisponibilite"]["centrale"],
            result["moins_indisponibilite"]["indisponibilite"]
        ))
    conn.commit()


def insert_taux_indisponibilite_parc(conn, results):
    with conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE taux_indisponibilite_parc RESTART IDENTITY;")
        sql = """
        INSERT INTO taux_indisponibilite_parc (
            taux
        )
        VALUES (%s)
        """

        for _, value in results:
            cur.execute(sql, (
                value["taux"],
            ))
    conn.commit()


def insert_taux_indisponibilite_centrale(conn, results):
    with conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE taux_indisponibilite_centrale RESTART IDENTITY;")
        sql = """
        INSERT INTO taux_indisponibilite_centrale (
            centrale,
            taux
        )
        VALUES (%s, %s)
        """

        for centrale, value in results:
            cur.execute(sql, (
                centrale,
                value["taux"],
            ))

    conn.commit()

def insert_taux_indisponibilite_tranche(conn, results):
    with conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE taux_indisponibilite_tranche RESTART IDENTITY;")
        sql = """
        INSERT INTO taux_indisponibilite_tranche (
            tranche,
            taux
        )
        VALUES (%s, %s)
        """

        for tranche, value in results:
            cur.execute(sql, (
                tranche,
                value["taux"],
            ))

    conn.commit()


def insert_centrales(conn, centrales):
    with conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE centrales RESTART IDENTITY;")
        sql = """
        INSERT INTO centrales (
            tri, centrale, tranche, filiere, combustible, contrat_programme,
            date_mise_en_service, puissance_installee, puissance_min, unite,
            latitude, longitude, region, departement, commune, sous_filiere,
            reserve_secondaire_maximale
        ) VALUES (
            %(tri)s, %(centrale)s, %(tranche)s, %(filiere)s, %(combustible)s,
            %(contrat_programme)s, %(date_mise_en_service)s, %(puissance_installee)s,
            %(puissance_min)s, %(unite)s, %(latitude)s, %(longitude)s,
            %(region)s, %(departement)s, %(commune)s, %(sous_filiere)s,
            %(reserve_secondaire_maximale)s
        )
        """
        for row in centrales:
            cur.execute(sql, row)
    conn.commit()