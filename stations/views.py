from django.http import JsonResponse

from .services import *


def get_near_stations(request):
    latitude = float(request.GET.get('lat'))
    longitude = float(request.GET.get('lng'))
    nearby_stations = fetch_near_stations(latitude, longitude)
    return JsonResponse({'near_stations': nearby_stations})


def get_station_data(request):
    station_id = str(request.GET.get('id'))
    station_data_temp = fetch_station_data(station_id)
    if not station_data_temp:
        return JsonResponse({'error': '정류소 데이터를 찾을 수 없습니다.'}, status=404)
    station_data = station_data_temp[0]
    # 총 주차 대수: station_data['parkingBikeTotCnt']
    return JsonResponse(station_data, safe=False)


def get_all_stations_data(request):
    stations = fetch_all_stations_data()
    return JsonResponse(stations, safe=False)
