import requests
from geopy.distance import geodesic
from django.http import JsonResponse
import params as pa

def geocoding(address):
    url = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"
    headers = {
        "X-NCP-APIGW-API-KEY-ID": pa.naver_client_id,
        "X-NCP-APIGW-API-KEY": pa.naver_client_secret
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

def get_near_stations(request):
    # 출발지 주소
    address = request.GET.get('address')
    latitude, longitude = geocoding(address)
    departure_location = (latitude, longitude)

    # 따릉이 API 호출
    url = f'http://openapi.seoul.go.kr:8088/{pa.tta_api_key}/json/bikeList/1/1000/'
    response = requests.get(url)
    if response.status_code != 200:
        return JsonResponse({'error': '따릉이 API 호출 실패'}, status=500)

    data = response.json()
    stations = data['rentBikeStatus']['row']

    # 반경 1km 내 대여소 필터링
    within_1km = []
    for station in stations:
        station_location = (float(station['stationLatitude']), float(station['stationLongitude']))
        distance = geodesic(departure_location, station_location).meters
        if distance <= 1000:  # 반경 1km 이내인지 확인
            within_1km.append({
                'stationName': station['stationName'],
                'latitude': station['stationLatitude'],
                'longitude': station['stationLongitude'],
                'distance': distance,
                'bikesAvailable': station['parkingBikeTotCnt'],
                'totalRacks': station['rackTotCnt']
            })

    # 가까운 대여소 정보 반환
    within_1km.sort(key=lambda x: x['distance'])  # 거리순 정렬
    return JsonResponse({'stations': within_1km})
