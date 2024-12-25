import requests

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
