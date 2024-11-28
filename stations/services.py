import requests
from geopy.distance import geodesic

import params as pa


def fetch_all_stations_data():
    url = f'http://openapi.seoul.go.kr:8088/{pa.SEOUL_API_KEY}/json/bikeList/1/1000/'
    try:
        response = requests.get(url)
        response.raise_for_status()  # HTTP 상태 코드가 200이 아니면 예외 발생
        return response.json().get('rentBikeStatus', {}).get('row', [])
    except Exception as e:
        print(f"Error fetching station data: {e}")
        return []


def fetch_station_data(station_id):
    url = f'http://openapi.seoul.go.kr:8088/{pa.SEOUL_API_KEY}/json/bikeList/1/1/{station_id}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get('rentBikeStatus', {}).get('row', [])
    except Exception as e:
        print(f"Error fetching station data: {e}")
        return []


def geocoding(address):
    url = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"
    headers = {
        "X-NCP-APIGW-API-KEY-ID": pa.NAVER_CLIENT_ID,
        "X-NCP-APIGW-API-KEY": pa.NAVER_CLIENT_SECRET
    }
    params = {"query": address}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        if data['addresses']:
            latitude = float(data['addresses'][0]['y'])
            longitude = float(data['addresses'][0]['x'])
            return latitude, longitude
        else:
            return None, None
    else:
        return None, None


def fetch_near_stations(latitude, longitude):
    radius = 500  # 반경 500m
    searching_location = (latitude, longitude)

    stations = fetch_all_stations_data()
    within_radius = []

    for station in stations:
        station_location = (float(station['stationLatitude']), float(station['stationLongitude']))
        distance = geodesic(searching_location, station_location).meters
        if distance <= radius:
            within_radius.append({
                'stationName': station['stationName'],
                'latitude': station['stationLatitude'],
                'longitude': station['stationLongitude'],
                'distance': distance,
                'bikesAvailable': station['parkingBikeTotCnt'],
                'totalRacks': station['rackTotCnt']
            })

    return sorted(within_radius, key=lambda x: x['distance'])
