import time

import requests
from geopy.distance import geodesic

import params as pa


# parameter 정보
# 1	rackTotCnt	거치대개수
# 2	stationName	대여소이름
# 3	parkingBikeTotCnt	자전거주차총건수
# 4	shared	거치율
# 5	stationLatitude	위도
# 6	stationLongitude	경도
# 7	stationId	대여소ID


# 전체 대여소 데이터 가져옴
def get_all_stations_data():
    base_url = f'http://openapi.seoul.go.kr:8088/{pa.SEOUL_API_KEY}/json/bikeList/'
    start = 1
    end = 500
    all_data = []

    while True:
        url = f"{base_url}{start}/{end}/"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()

            data = response.json()

            rows = data.get('rentBikeStatus', {}).get('row', [])
            if not rows:
                break

            filtered_data = [
                station for station in rows
                if float(station.get('stationLatitude', 0)) != 0 and float(station.get('stationLongitude', 0)) != 0
            ]
            all_data.extend(filtered_data)

            start = end + 1
            end = start + 499

        except requests.exceptions.RequestException as e:
            print(f"HTTP 요청 오류: {e}")
            break
        except ValueError as e:
            print(f"JSON 파싱 오류: {e}")
            break
        except KeyError as e:
            print(f"데이터 구조 키 오류: {e}")
            break

    return all_data


# station id에 해당하는 대여소 1개 데이터 가져옴
def get_station_data(station_id):
    url = f'http://openapi.seoul.go.kr:8088/{pa.SEOUL_API_KEY}/json/bikeList/1/1/{station_id}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get('rentBikeStatus', {}).get('row', [])
    except Exception as e:
        print(f"Error: {e}")
        return []


# 주소를 입력하면 위도, 경도로 변환
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

    return None, None


# 위도, 경도를 입력하면 주소로 변환
def reverse_geocoding(latitude, longitude):
    url = "https://naveropenapi.apigw.ntruss.com/map-reversegeocode/v2/gc"
    headers = {
        "X-NCP-APIGW-API-KEY-ID": pa.NAVER_CLIENT_ID,
        "X-NCP-APIGW-API-KEY": pa.NAVER_CLIENT_SECRET
    }
    params = {
        "coords": f"{longitude},{latitude}",
        "orders": "roadaddr",
        "output": "json"
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get("results"):
            address_info = data["results"][0]
            region = address_info.get("region", {})
            land = address_info.get("land", {})

            road_address = (region.get("area1", {}).get("name", "") + " " +
                            region.get("area2", {}).get("name", "") + " " +
                            land.get("name", "") + " " +
                            land.get("number1", ""))
            if land.get("number2"):
                road_address += "-" + land.get("number2")
            return road_address.strip()
        else:
            return "주소"

    except Exception as e:
        print(f"API 요청 중 에러 발생: {e}")
        print(f"응답 내용: {response.text}")
        return ""


# 위도, 경도, 반경을 입력하면 해당 반경 내의 대여소 목록 반환 (거리 순 정렬)
def get_near_stations(latitude, longitude, radius):
    searching_location = (latitude, longitude)

    # 모든 대여소 데이터 가져오기
    stations = get_all_stations_data()
    time.sleep(1)
    if not stations:
        print("따릉이 대여소 데이터가 비어 있습니다.")
        return []

    within_radius = []

    for station in stations:
        try:
            station_location = (float(station['stationLatitude']), float(station['stationLongitude']))
            distance = geodesic(searching_location, station_location).meters
            if distance <= radius:
                within_radius.append({
                    'stationName': station['stationName'],
                    'distance': distance,
                    'latitude': station['stationLatitude'],
                    'longitude': station['stationLongitude'],
                    'bikesAvailable': station['parkingBikeTotCnt'],
                })
        except (ValueError, KeyError) as e:
            print(f"대여소 데이터 처리 중 오류: {e}")
            continue

    if not within_radius:
        print(f"해당 위치 근처에 따릉이 대여소가 없습니다: {reverse_geocoding(latitude, longitude)} ({latitude}, {longitude})")
        for station in stations:
            try:
                station_location = (float(station['stationLatitude']), float(station['stationLongitude']))
                distance = geodesic(searching_location, station_location).meters
                print(f"대여소: {station['stationName']}, 거리: {distance}m")
            except (ValueError, KeyError) as e:
                print(f"대여소 거리 계산 중 오류: {e}")
        return []

    return sorted(within_radius, key=lambda x: x['distance'])
