from django.http import JsonResponse
from django.shortcuts import render

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
    station = station_data_temp[0]
    return render(request, 'stations/station_info.html', {'station': station})


def station_list_view(request):
    data = get_all_stations_data()

    stations = [
        {
            'name': station.get('stationName', ''),
            'location': f"{station.get('stationLatitude')}, {station.get('stationLongitude')}",
            'id': station.get('stationId'),
        }
        for station in data
    ]
    return render(request, 'stations/station_list.html', {'stations': stations})

