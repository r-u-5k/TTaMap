import requests
from django.http import JsonResponse
from geopy.distance import geodesic

import params as pa

def get_near_stations(request):
    # 출발지 주소
    latitude = float(request.GET.get('latitude'))
    longitude = float(request.GET.get('longitude'))

    departure_location = (latitude, longitude)

    # 따릉이 API 호출
    url = f'http://openapi.seoul.go.kr:8088/{pa.SEOUL_API_KEY}/json/bikeList/1/1000/'
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
        if distance <= 1000:
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
