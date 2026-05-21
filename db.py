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
    return psycopg2.connect(**DB_CONFIG)


def create_tables(conn):
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
