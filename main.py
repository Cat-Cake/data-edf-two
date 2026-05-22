from download_file import download_data
from prepare_clean_csv import prepare_clean_csv
from stats_centrale import run_stats_centrale
from stats_centrale_meilleur_prod import run_stats_centrale_meilleur_prod
from stats_centrale_moins_bonne_prod import run_stats_centrale_moins_bonne_prod
from stats_centrale_plus_indis_prod import run_stats_centrale_plus_indis_prod
from stats_centrale_tranche import run_stats_centrale_tranche
from stats_parc import run_stats_parc
from stats_prod_centrale_annee import run_prod_centrale_annee
from stats_prod_parc_annee import run_prod_parc_annee
from stats_indis_parc_annee import run_indis_parc_annee
from stats_indis_prod_zero import run_indis_prod_zero
from stats_indis_prod_sup_zero import run_indis_prod_sup_zero
from db import (
    get_connection, create_tables,
    insert_stats_parc, insert_stats_centrale, insert_stats_centrale_tranche,
    insert_prod_parc_annee, insert_prod_centrale_annee, insert_indis_parc_annee,
    insert_indis_prod_zero, insert_indis_prod_sup_zero,
)


def main():
    download_data("edf_data.csv")
    prepare_clean_csv("edf_data.csv", "edf_clean.csv")

    min_max_mean_parc = run_stats_parc("edf_clean.csv")
    min_max_mean_centrale = run_stats_centrale("edf_clean.csv")
    min_max_mean_centrale_tranche = run_stats_centrale_tranche("edf_clean.csv")
    total_parc_annee = run_prod_parc_annee("edf_clean.csv")
    total_centrale_annee = run_prod_centrale_annee("edf_clean.csv")
    total_indis_parc_annee = run_indis_parc_annee("edf_clean.csv")
    total_indis_prod_zero = run_indis_prod_zero("edf_data.csv")
    total_indis_prod_sup_zero = run_indis_prod_sup_zero("edf_clean.csv")
    centrale_meilleur_prod = run_stats_centrale_meilleur_prod("edf_clean.csv")
    centrale_moin_bonne_prod = run_stats_centrale_moins_bonne_prod("edf_clean.csv")
    centrale_plus_indis_prod = run_stats_centrale_plus_indis_prod("edf_clean.csv")
    centrale_moins_indis_prod = run_stats_centrale_moins_bonne_prod("edf_clean.csv")

    print("\nRésultat ensemble du parc :")
    for key, value in min_max_mean_parc:
        print(key, value)

    print("\nRésultat chaque centrale :")
    for key, value in min_max_mean_centrale:
        print(key, value)

    print("\nRésultat chaque tranche de chaque centrale :")
    for key, value in min_max_mean_centrale_tranche:
        print(key, value)

    print("\nRésultat total de production sur l'ensemble du parc sur une année :")
    for key, value in total_parc_annee:
        print(key, value)

    print("\nRésultat total de production par centrale sur une année :")
    for key, value in total_centrale_annee:
        print(key, value)

    print("\nRésultat total d'indisponibilité du parc sur une année :")
    for key, value in total_indis_parc_annee:
        print(key, value)

    print("\nRésultat total d'indisponibilité à production zéro :")
    for key, value in total_indis_prod_zero:
        print(key, value)

    print("\nRésultat total d'indisponibilité à production supérieure à zéro :")
    for key, value in total_indis_prod_sup_zero:
        print(key, value)

    print("\nRésultat centrale meilleur production sur l’année :")
    for key, value in centrale_meilleur_prod:
        print(key, value)

    print("\nRésultat centrale moins bonne production sur l’année :")
    for key, value in centrale_moin_bonne_prod:
        print(key, value)

    print("\nRésultat centrale plus d’indisponibilité sur l’année :")
    for key, value in centrale_plus_indis_prod:
        print(key, value)

    print("\nRésultat centrale moins d’indisponibilité sur l’année :")
    for key, value in centrale_moins_indis_prod:
        print(key, value)


    print("\nEnregistrement en base...")
    conn = get_connection()
    create_tables(conn)
    insert_stats_parc(conn, min_max_mean_parc)
    insert_stats_centrale(conn, min_max_mean_centrale)
    insert_stats_centrale_tranche(conn, min_max_mean_centrale_tranche)
    insert_prod_parc_annee(conn, total_parc_annee)
    insert_prod_centrale_annee(conn, total_centrale_annee)
    insert_indis_parc_annee(conn, total_indis_parc_annee)
    insert_indis_prod_zero(conn, total_indis_prod_zero)
    insert_indis_prod_sup_zero(conn, total_indis_prod_sup_zero)
    conn.close()
    print("Données enregistrées.")


if __name__ == "__main__":
    main()
