import requests

URL_EDF = "https://opendata.edf.fr/data-fair/api/v1/datasets/haqk2fpmdz21sjiwhva-0n2x/data-files/Export_toutes_versions-full.csv"
URL_CENTRALES = "https://opendata.edf.fr/data-fair/api/v1/datasets/ohco3c11wq2fz546oumq6oxr/data-files/Centrales%20de%20production%20nucl%C3%A9aire%20d'EDF%20SA_02072024-full.csv"
URL_HIST = "https://opendata.edf.fr/data-fair/api/v1/datasets/6jf-zbbwhqgpw2vbto1k9yhc/lines?format=csv&size=10000&filiere=Nucl%C3%A9aire&sort=annee"


def _download(url, filename):
    response = requests.get(url, stream=True, timeout=60)
    if response.status_code != 200:
        raise Exception(f"Erreur téléchargement : {response.status_code}")
    with open(filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    print(f"Download finished: {filename}")


def download_data(filename="edf_data.csv"):
    print("Downloading CSV...")
    _download(URL_EDF, filename)


def download_centrales(filename="centrales.csv"):
    print("Downloading centrales CSV...")
    _download(URL_CENTRALES, filename)


def download_hist(filename="edf_hist.csv"):
    print("Downloading historical production CSV...")
    _download(URL_HIST, filename)