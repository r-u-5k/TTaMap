import urllib.parse
from geopy.distance import geodesic
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
        "startX": start_lng,
        "startY": start_lat,
        "endX": end_lng,
        "endY": end_lat,
        "startName": urllib.parse.quote(reverse_geocoding(start_lat, start_lng) or "출발지", encoding='utf-8'),
        "endName": urllib.parse.quote(reverse_geocoding(end_lat, end_lng) or "도착지", encoding='utf-8'),
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

    try:
        data = {
            "startX": start_lng,
            "startY": start_lat,
            "endX": end_lng,
            "endY": end_lat,
            "startName": urllib.parse.quote(reverse_geocoding(start_lat, start_lng) or "출발지", encoding='utf-8'),
            "endName": urllib.parse.quote(reverse_geocoding(end_lat, end_lng) or "도착지", encoding='utf-8'),
        }

        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        for feature in result.get("features", []):
            properties = feature.get("properties", {})
            if "totalTime" in properties:
                properties["totalTime"] = properties["totalTime"] // 4
            if "time" in properties:
                properties["time"] = properties["time"] // 4

        result["type"] = "bike"
        return result

    except requests.exceptions.RequestException as e:
        print(f"HTTP 요청 오류: {e}")
        raise
    except ValueError as e:
        print(f"JSON 파싱 오류: {e}")
        raise
    except Exception as e:
        print(f"기타 오류: {e}")
        raise


# 출발지 → 출발지 주변 따릉이 대여소(A) (도보)
# 출발지 주변 따릉이 대여소(A) → 대중교통 승차지 주변 따릉이 대여소(B) (따릉이)
# 대중교통 승차지 → 대중교통 하차지 (대중교통)
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
    bike_stations_A = get_near_stations(start_lat, start_lng, 300)
    # 대중교통 승차지 주변 따릉이 대여소
    bike_stations_B = get_near_stations(start_pt_station_lat, start_pt_station_lng, 300)

    distance_start2pt = geodesic((start_lat, start_lng), (start_pt_station_lat, start_pt_station_lng)).meters

    if bike_stations_A and bike_stations_B and distance_start2pt > 100:
        bike_station_A = bike_stations_A[0]
        bike_station_A_lat = bike_station_A['latitude']
        bike_station_A_lng = bike_station_A['longitude']
        bike_station_B = bike_stations_B[0]
        bike_station_B_lat = bike_station_B['latitude']
        bike_station_B_lng = bike_station_B['longitude']
        route_start2A = get_walk_route(start_lat, start_lng, bike_station_A_lat, bike_station_A_lng)
        distance_A2B = geodesic((bike_station_A_lat, bike_station_A_lng), (bike_station_B_lat, bike_station_B_lng)).meters
        if distance_A2B > 100:
            route_A2B = get_bike_route(bike_station_A_lat, bike_station_A_lng, bike_station_B_lat, bike_station_B_lng)
            route_A2B["startBikeStation"] = bike_station_A["stationName"]
            route_A2B["startBikeLat"] = bike_station_A_lat
            route_A2B["startBikeLng"] = bike_station_A_lng
            route_A2B["endBikeStation"] = bike_station_B["stationName"]
            route_A2B["endBikeLat"] = bike_station_B_lat
            route_A2B["endBikeLng"] = bike_station_B_lng
            full_route.append(route_start2A)
            full_route.append(route_A2B)
        else:
            route_start2pt = get_walk_route(start_lat, start_lng, start_pt_station_lat, start_pt_station_lng)
            route_start2pt["startLat"] = start_lat
            route_start2pt["startLng"] = start_lng
            route_start2pt["endLat"] = start_pt_station_lat
            route_start2pt["endLng"] = start_pt_station_lng
            full_route.append(route_start2pt)
    else:
        # 출발지에서 대중교통 승차지까지 도보로 이동
        route_start2pt = get_walk_route(start_lat, start_lng, start_pt_station_lat, start_pt_station_lng)
        full_route.append(route_start2pt)
        print("주변에 따릉이 대여소가 없거나 출발지에서 대중교통 승차지까지 100m 이하")

    # 대중교통 경로
    route_B2C = get_odsay_route(start_pt_station_lat, start_pt_station_lng, end_pt_station_lat, end_pt_station_lng)
    full_route.append(route_B2C)

    distance_pt2end = geodesic((end_pt_station_lat, end_pt_station_lng), (end_lat, end_lng)).meters

    # 대중교통 하차지 주변 따릉이 대여소
    bike_stations_C = get_near_stations(end_pt_station_lat, end_pt_station_lng, 300)
    # 도착지 주변 따릉이 대여소
    bike_stations_D = get_near_stations(end_lat, end_lng, 300)

    if (bike_stations_C and bike_stations_D) and distance_pt2end > 100:
        bike_station_C = bike_stations_C[0]
        bike_station_C_lat = bike_station_C['latitude']
        bike_station_C_lng = bike_station_C['longitude']
        bike_station_D = bike_stations_D[0]
        bike_station_D_lat = bike_station_D['latitude']
        bike_station_D_lng = bike_station_D['longitude']
        distance_C2D = geodesic((bike_station_C_lat, bike_station_C_lng), (bike_station_D_lat, bike_station_D_lng))
        if distance_C2D > 100:
            route_C2D = get_bike_route(bike_station_C_lat, bike_station_C_lng, bike_station_D_lat, bike_station_D_lng)
            route_C2D["startBikeStation"] = bike_station_C["stationName"]
            route_C2D["startBikeLat"] = bike_station_C_lat
            route_C2D["startBikeLng"] = bike_station_C_lng
            route_C2D["endBikeStation"] = bike_station_D["stationName"]
            route_C2D["endBikeLat"] = bike_station_D_lat
            route_C2D["endBikeLng"] = bike_station_D_lng
            route_D2end = get_walk_route(bike_station_D_lat, bike_station_D_lng, end_lat, end_lng)
            full_route.append(route_C2D)
            full_route.append(route_D2end)
        else:
            route_pt2end = get_walk_route(end_pt_station_lat, end_pt_station_lng, end_lat, end_lng)
            full_route.append(route_pt2end)
    else:
        # 대중교통 하차지에서 도착지까지 도보로 이동
        route_pt2end = get_walk_route(end_pt_station_lat, end_pt_station_lng, end_lat, end_lng)
        full_route.append(route_pt2end)
        print("주변에 따릉이 대여소가 없거나 대중교통 하차지에서 도착지까지 100m 이하")

    return full_route


def get_simple_route(start_lat, start_lng, end_lat, end_lng):
    full_route = get_full_route(start_lat, start_lng, end_lat, end_lng)

    total_distance = 0.0
    total_time = 0
    steps = []

    for route in full_route:
        if "type" in route and route["type"] in ["walk", "bike"]:
            mode = route["type"]
            start_bike_station = route.get("startBikeStation", "")
            start_bike_station_lat = route.get("startBikeLat", "")
            start_bike_station_lng = route.get("endBikeLat", "")
            end_bike_station = route.get("endBikeStation", "")
            end_bike_station_lat = route.get("endBikeLat", "")
            end_bike_station_lng = route.get("endBikeLng", "")

            route_distance = 0.0
            route_time_sec = 0
            for f in route.get("features", []):
                if f.get("geometry", {}).get("type") == "LineString":
                    distance = f.get("properties", {}).get("distance", 0)
                    time = f.get("properties", {}).get("time", 0)
                    route_distance += distance
                    route_time_sec += time
                    if mode == "walk":
                        steps.append({
                            "mode": mode,
                            "distance": distance,
                            "time": time,
                            "startLat": start_lat,
                            "startLng": start_lng,
                            "endLat": end_lat,
                            "endLng": end_lng,
                        })
                    elif mode == "bike":
                        steps.append({
                            "mode": mode,
                            "distance": distance,
                            "time": time,
                            "startBikeStation": start_bike_station,
                            "endBikeStation": end_bike_station,
                            "startBikeLat": start_bike_station_lat,
                            "startBikeLng": start_bike_station_lng,
                            "endBikeLat": end_bike_station_lat,
                            "endBikeLng": end_bike_station_lng,
                        })
            total_distance += route_distance
            total_time += route_time_sec

        elif "result" in route and "path" in route["result"]:
            path = route["result"]["path"][0]
            info = path["info"]
            transit_distance = info.get("totalDistance", 0)
            transit_time_min = info.get("totalTime", 0)
            # trafficType: 1(지하철), 2(버스), 3(도보)
            for sp in path.get("subPath", []):
                ttype = sp.get("trafficType", 0)
                sp_distance = sp.get("distance", 0)
                sp_time = sp.get("sectionTime", 0)
                step_mode = "transit" if ttype in [1, 2] else "walk"

                start_station = sp.get("startName", "") if step_mode == "transit" else ""
                end_station = sp.get("endName", "") if step_mode == "transit" else ""
                start_station_lat = sp.get("startY", "")
                start_station_lng = sp.get("startX", "")
                end_station_lat = sp.get("endY", "")
                end_station_lng = sp.get("endX", "")

                steps.append({
                    "mode": step_mode,
                    "distance": sp_distance,
                    "time": sp_time * 60,
                    "startStation": start_station,
                    "endStation": end_station,
                    "startStationLat": start_station_lat,
                    "startStationLng": start_station_lng,
                    "endStationLat": end_station_lat,
                    "endStationLng": end_station_lng,
                })
            total_distance += transit_distance
            total_time += transit_time_min * 60

    filtered_steps = []
    for step in steps:
        if not (step["mode"] == "walk" and step["distance"] == 0 and step["time"] == 0):
            filtered_steps.append(step)

    steps = filtered_steps

    merged_steps = []
    for step in steps:
        if merged_steps and merged_steps[-1]["mode"] == step["mode"]:
            # 같은 모드면 distance, time 합산
            merged_steps[-1]["distance"] += step["distance"]
            merged_steps[-1]["time"] += step["time"]

            # 만약 대중교통 구간이라면 startStation은 유지, endStation은 새 구간의 endStation으로 업데이트
            if step["mode"] == "transit":
                merged_steps[-1]["endStation"] = step["endStation"]
        else:
            # 모드가 다르거나 merged_steps가 비어있으면 새로 추가
            merged_steps.append(step)

    steps = merged_steps

    summary = {
        "totalDistance": total_distance,
        "totalTime": total_time,
        "steps": steps
    }
    print("경로 요약:", summary)
    return summary
