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
            response = requests.get(url)
            response.raise_for_status()  # HTTP 상태 코드 확인
            data = response.json().get('rentBikeStatus', {}).get('row', [])

            if not data:  # 데이터가 더 없으면 종료
                break

            filtered_data = [station for station in data if float(station['stationLatitude']) != 0]  # 위도값이 0인 데이터는 제거
            all_data.extend(filtered_data)

            start = end + 1
            end = start + 499

        except Exception as e:
            print(f"Error: {e}")
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
            road_address = (address_info.get("region", {}).get("area1", {}).get("name", "") + " " +
                            address_info.get("region", {}).get("area2", {}).get("name", "") + " " +
                            address_info.get("region", {}).get("area3", {}).get("name", "") + " " +
                            address_info.get("region", {}).get("area4", {}).get("name", "") + " " +
                            address_info.get("land", {}).get("name", "") + " " +
                            address_info.get("land", {}).get("number1", "") + " " +
                            address_info.get("land", {}).get("number2", ""))
            return road_address.strip()
        else:
            return ""

    except requests.exceptions.RequestException as e:
        print(f"API 요청 중 에러 발생: {e}")
        return ""


# 위도, 경도를 입력하면 가까운 대여소 목록 반환 (거리 순 정렬)
def get_near_stations(latitude, longitude):
    radius = 1000  # 반경 1km
    searching_location = (latitude, longitude)

    stations = get_all_stations_data()
    within_radius = []

    for station in stations:
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
    if not within_radius:
        print(f"해당 위치 근처에 따릉이 대여소가 없습니다: ({latitude}, {longitude})")
        raise ValueError("따릉이 대여소를 찾을 수 없습니다.")
    return sorted(within_radius, key=lambda x: x['distance'])
