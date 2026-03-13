import json

import requests

url = "https://opendata.edf.fr/data-fair/api/v1/datasets/indisponibilites-des-moyens-de-production-edf-sa/lines"


def import_data(page):
    parameters = {"page": page,
                  "size": 500}
    response = requests.get(url, params=parameters)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")


def main():
    all_data = []
    page = 1

    while True:
        print("Downloading page", page)
        data = import_data(page)

        if data is None or len(data['results']) == 0:
            break

        all_data.extend(data['results'])
        page += 1
    print('Total records', len(all_data))

    with open('edf_records.json', 'w') as outfile:
        json.dump(all_data, outfile)


if __name__ == "__main__":
    main()
