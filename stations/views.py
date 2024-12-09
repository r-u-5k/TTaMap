from django.http import JsonResponse

from .services import *


def near_stations_view(request):
    latitude = float(request.GET.get('lat'))
    longitude = float(request.GET.get('lng'))
    near_stations = get_near_stations(latitude, longitude, 500)
    return JsonResponse(near_stations, safe=False)


def station_data_view(request):
    station_id = str(request.GET.get('id'))
    station_data_temp = get_station_data(station_id)
    if not station_data_temp:
        return JsonResponse({'error': '정류소 데이터를 찾을 수 없습니다.'}, status=404)
    station_data = station_data_temp[0]
    # 주차된 따릉이 대수: station_data['parkingBikeTotCnt']
    return JsonResponse(station_data, safe=False)


def all_stations_data_view(request):
    stations = get_all_stations_data()
    return JsonResponse(stations, safe=False)
