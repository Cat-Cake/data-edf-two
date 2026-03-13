import json
import requests

from download_file import download_data
from prepare_clean_csv import prepare_clean_csv
from stats_parc import MRStatsParc, run_stats_parc


def main():
    download_data("edf_data.csv")
    prepare_clean_csv("edf_data.csv", "edf_clean.csv")

    results = run_stats_parc("edf_clean.csv")

    print("\nRésultat MapReduce :")
    for key, value in results:
        print(key, value)


if __name__ == "__main__":
    main()
