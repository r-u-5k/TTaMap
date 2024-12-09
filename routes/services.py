import urllib.parse

import requests

import params as pa
from stations.services import get_near_stations, reverse_geocoding


# Odsay 경로
def get_odsay_route(start_lat, start_lng, end_lat, end_lng):
    api_key = pa.ODSAY_API_KEY
    encoded_api_key = urllib.parse.quote(api_key, encoding='utf-8')
    url_info = f"https://api.odsay.com/v1/api/searchPubTransPathT?SY={start_lat}&SX={start_lng}&EY={end_lat}&EX={end_lng}&apiKey={encoded_api_key}"

    response = requests.get(url_info, headers={"Content-type": "application/json"})

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Odsay API request failed with status {response.status_code}")


# 도보 이동 경로
def get_walk_route(start_lat, start_lng, end_lat, end_lng):
    api_key = pa.TMAP_API_KEY
    url = "https://apis.openapi.sk.com/tmap/routes/pedestrian?version=1"
    headers = {
        "Accept": "application/json",
        "appKey": api_key,
        "Content-Type": "application/json"
    }
    data = {
        "startY": start_lat,
        "startX": start_lng,
        "endY": end_lat,
        "endX": end_lng,
        "speed": 4,
        "startName": urllib.parse.quote(reverse_geocoding(start_lat, start_lng), encoding='utf-8'),
        "endName": urllib.parse.quote(reverse_geocoding(end_lat, end_lng), encoding='utf-8'),
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"TMAP Walk API request failed with status {response.status_code}")


# 자전거 이동 경로
def get_bike_route(start_lat, start_lng, end_lat, end_lng):
    api_key = pa.TMAP_API_KEY
    url = "https://apis.openapi.sk.com/tmap/routes/pedestrian?version=1"
    headers = {
        "Accept": "application/json",
        "appKey": api_key,
        "Content-Type": "application/json"
    }
    data = {
        "startY": start_lat,
        "startX": start_lng,
        "endY": end_lat,
        "endX": end_lng,
        "startName": urllib.parse.quote(reverse_geocoding(start_lat, start_lng), encoding='utf-8'),
        "endName": urllib.parse.quote(reverse_geocoding(end_lat, end_lng), encoding='utf-8'),
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()

        for feature in result.get("features", []):
            properties = feature.get("properties", {})
            if "totalTime" in properties:
                properties["totalTime"] = properties["totalTime"] // 4  # 전체 이동 시간 업데이트

            if "time" in properties:
                properties["time"] = properties["time"] // 4  # 구간별 이동 시간 업데이트

        return result
    else:
        raise Exception(f"TMAP Bike API request failed with status {response.status_code}")


# 출발지 → 출발지 주변 따릉이 대여소(A) (도보)
# 출발지 주변 따릉이 대여소(A) → 대중교통 승차지 주변 따릉이 대여소(B) (따릉이)
# 대중교통 승차지 주변 따릉이 대여소(B) → 대중교통 하차지 주변 따릉이 대여소(C) (대중교통 API)
# 대중교통 하차지 주변 따릉이 대여소(C) → 도착지 주변 따릉이 대여소(D) (따릉이)
# 도착지 주변 따릉이 대여소(D) → 도착지 (도보)

def get_full_route(start_lat, start_lng, end_lat, end_lng):
    data = get_odsay_route(start_lat, start_lng, end_lat, end_lng)

    start_pt_station = data['result']['path'][0]['subPath'][1]
    start_pt_station_lat = start_pt_station['startY']
    start_pt_station_lng = start_pt_station['startX']

    end_pt_station = data['result']['path'][0]['subPath'][-2]
    end_pt_station_lat = end_pt_station['endY']
    end_pt_station_lng = end_pt_station['endX']

    # 출발지 주변 따릉이 대여소
    bike_station_A = get_near_stations(start_lat, start_lng)[0]
    bike_station_A_lat = bike_station_A['latitude']
    bike_station_A_lng = bike_station_A['longitude']
    # 대중교통 승차지 주변 따릉이 대여소
    bike_station_B = get_near_stations(start_pt_station_lat, start_pt_station_lng)[0]
    bike_station_B_lat = bike_station_B['latitude']
    bike_station_B_lng = bike_station_B['longitude']
    # 대중교통 하차지 주변 따릉이 대여소
    bike_station_C = get_near_stations(end_pt_station_lat, end_pt_station_lng)[0]
    bike_station_C_lat = bike_station_C['latitude']
    bike_station_C_lng = bike_station_C['longitude']
    # 도착지 주변 따릉이 대여소
    bike_station_D = get_near_stations(end_lat, end_lng)[0]
    bike_station_D_lat = bike_station_D['latitude']
    bike_station_D_lng = bike_station_D['longitude']

    route_start2A = get_walk_route(start_lat, start_lng, bike_station_A_lat, bike_station_A_lng)
    route_A2B = get_bike_route(bike_station_A_lat, bike_station_A_lng, bike_station_B_lat, bike_station_B_lng)
    route_B2C = get_odsay_route(bike_station_B_lat, bike_station_B_lng, bike_station_C_lat, bike_station_C_lng)
    route_C2D = get_bike_route(bike_station_C_lat, bike_station_C_lng, bike_station_D_lat, bike_station_D_lng)
    route_D2end = get_walk_route(bike_station_D_lat, bike_station_D_lng, end_lat, end_lng)

    full_route = [route_start2A, route_A2B, route_B2C, route_C2D, route_D2end]
    return full_route
