import json
import requests

from download_file import download_data
from prepare_clean_csv import prepare_clean_csv
from stats_centrale import run_stats_centrale
from stats_centrale_tranche import run_stats_centrale_tranche
from stats_parc import run_stats_parc
from stats_prod_centrale_annee import run_prod_centrale_annee
from stats_prod_parc_annee import run_prod_parc_annee


def main():
    download_data("edf_data.csv")
    prepare_clean_csv("edf_data.csv", "edf_clean.csv")

    min_max_mean_parc = run_stats_parc("edf_clean.csv")
    min_max_mean_centrale = run_stats_centrale("edf_clean.csv")
    min_max_mean_centrale_tranche = run_stats_centrale_tranche("edf_clean.csv")
    total_parc_annee = run_prod_parc_annee("edf_clean.csv")
    total_centrale_annee = run_prod_centrale_annee("edf_clean.csv")

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


if __name__ == "__main__":
    main()
