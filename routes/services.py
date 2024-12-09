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
        result = response.json()
        result["type"] = "transit"
        return result
    else:
        raise Exception(f"Odsay API request failed with status {response.status_code}")


# 도보 이동 경로
def get_walk_route(start_lat, start_lng, end_lat, end_lng):
    url = "https://apis.openapi.sk.com/tmap/routes/pedestrian?version=1"
    headers = {
        "Accept": "application/json",
        "appKey": pa.TMAP_API_KEY,
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
        result["type"] = "walk"
        return result
    else:
        raise Exception(f"TMAP Walk API request failed with status {response.status_code}")


# 자전거 이동 경로
def get_bike_route(start_lat, start_lng, end_lat, end_lng):
    url = "https://apis.openapi.sk.com/tmap/routes/pedestrian?version=1"
    headers = {
        "Accept": "application/json",
        "appKey": pa.TMAP_API_KEY,
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

        result["type"] = "bike"

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

    full_route = []

    # 출발지 주변 따릉이 대여소
    bike_stations_A = get_near_stations(start_lat, start_lng, 500)
    # 대중교통 승차지 주변 따릉이 대여소
    bike_stations_B = get_near_stations(start_pt_station_lat, start_pt_station_lng, 500)

    if bike_stations_A and bike_stations_B:
        bike_station_A = bike_stations_A[0]
        bike_station_A_lat = bike_station_A['latitude']
        bike_station_A_lng = bike_station_A['longitude']
        bike_station_B = bike_stations_B[0]
        bike_station_B_lat = bike_station_B['latitude']
        bike_station_B_lng = bike_station_B['longitude']
        route_start2A = get_walk_route(start_lat, start_lng, bike_station_A_lat, bike_station_A_lng)
        route_A2B = get_bike_route(bike_station_A_lat, bike_station_A_lng, bike_station_B_lat, bike_station_B_lng)
        full_route.append(route_start2A)
        full_route.append(route_A2B)
    else:
        # 따릉이 대여소가 없으면 출발지에서 대중교통 승차지까지 도보로 이동
        route_start2B = get_walk_route(start_lat, start_lng, start_pt_station_lat, start_pt_station_lng)
        full_route.append(route_start2B)

    # 대중교통 경로
    route_B2C = get_odsay_route(start_pt_station_lat, start_pt_station_lng, end_pt_station_lat, end_pt_station_lng)
    full_route.append(route_B2C)

    # 대중교통 하차지 주변 따릉이 대여소
    bike_stations_C = get_near_stations(end_pt_station_lat, end_pt_station_lng, 500)
    # 도착지 주변 따릉이 대여소
    bike_stations_D = get_near_stations(end_lat, end_lng, 500)

    if bike_stations_C and bike_stations_D:
        bike_station_C = bike_stations_C[0]
        bike_station_C_lat = bike_station_C['latitude']
        bike_station_C_lng = bike_station_C['longitude']
        bike_station_D = bike_stations_D[0]
        bike_station_D_lat = bike_station_D['latitude']
        bike_station_D_lng = bike_station_D['longitude']
        route_C2D = get_bike_route(bike_station_C_lat, bike_station_C_lng, bike_station_D_lat, bike_station_D_lng)
        route_D2end = get_walk_route(bike_station_D_lat, bike_station_D_lng, end_lat, end_lng)
        full_route.append(route_C2D)
        full_route.append(route_D2end)
    else:
        # 따릉이 대여소가 없으면 출발지에서 대중교통 승차지까지 도보로 이동
        route_C2end = get_walk_route(end_pt_station_lat, end_pt_station_lng, end_lat, end_lng)
        full_route.append(route_C2end)

    return full_route


def get_simple_route(data_list):
    summary = []
    for data in data_list:
        data_type = data.get("type", "")

        # 도보/자전거 데이터 처리
        if data_type in ["walk", "bike"]:
            for feature in data.get("features", []):
                properties = feature.get("properties", {})
                geometry = feature.get("geometry", {})
                if properties and geometry:
                    summary.append({
                        "type": data_type,
                        "distance": properties.get("totalDistance", 0),
                        "time": properties.get("totalTime", 0),
                        "description": properties.get("description", ""),
                        "coordinates": geometry.get("coordinates", [])
                    })

        # 대중교통 데이터 처리
        elif data_type == "transit":
            for path in data.get("result", {}).get("path", []):
                for sub_path in path.get("subPath", []):
                    if sub_path.get("trafficType") == 1:  # 지하철
                        summary.append({
                            "type": "subway",
                            "line": sub_path.get("lane", [{}])[0].get("name", ""),
                            "start": sub_path.get("startName", ""),
                            "end": sub_path.get("endName", ""),
                            "distance": sub_path.get("distance", 0),
                            "time": sub_path.get("sectionTime", 0),
                            "stationCount": sub_path.get("stationCount", 0)
                        })
                    elif sub_path.get("trafficType") == 2:  # 버스
                        summary.append({
                            "type": "bus",
                            "line": sub_path.get("lane", [{}])[0].get("busNo", ""),
                            "start": sub_path.get("startName", ""),
                            "end": sub_path.get("endName", ""),
                            "distance": sub_path.get("distance", 0),
                            "time": sub_path.get("sectionTime", 0),
                            "stationCount": sub_path.get("stationCount", 0)
                        })
                    elif sub_path.get("trafficType") == 3:  # 도보
                        summary.append({
                            "type": "walk",
                            "distance": sub_path.get("distance", 0),
                            "time": sub_path.get("sectionTime", 0)
                        })

    return summary
