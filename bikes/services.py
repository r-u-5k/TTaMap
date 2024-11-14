import urllib.parse

import requests

import params as pa


def fetch_bikes():
    api_key = pa.tta_api_key
    url_info = f"http://openapi.seoul.go.kr:8088/{api_key}/json/bikeList/1/5/"

    response = requests.get(url_info, headers={"Content-type": "application/json"})

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API request failed with status {response.status_code}")
