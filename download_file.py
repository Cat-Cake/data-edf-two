import requests

URL = "https://opendata.edf.fr/data-fair/api/v1/datasets/haqk2fpmdz21sjiwhva-0n2x/data-files/Export_toutes_versions.csv"


def download_data(filename="edf_data.csv"):
    print("Downloading CSV...")

    response = requests.get(URL, stream=True, timeout=60)
    if response.status_code != 200:
        raise Exception(f"Erreur téléchargement : {response.status_code}")

    with open(filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    print(f"Download finished: {filename}")