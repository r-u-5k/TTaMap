import requests
import urllib.parse
import params as pa

def get_public_transport_route(departure_lat, departure_lon, arrival_lat, arrival_lon):
    api_key = pa.ODSAY_API_KEY
    encoded_api_key = urllib.parse.quote(api_key, encoding='utf-8')
    url_info = f"https://api.odsay.com/v1/api/searchPubTransPathT?SY={departure_lat}&SX={departure_lon}&EY={arrival_lat}&EX={arrival_lon}&apiKey={encoded_api_key}"

    response = requests.get(url_info, headers={"Content-type": "application/json"})

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API request failed with status {response.status_code}")
