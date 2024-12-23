import requests
from django.shortcuts import render
from django.http import JsonResponse
import params as pa
from .services import get_station_data, get_all_stations_data


def map_view(request):
    return render(request, 'maps/map.html')


def station_data_view(request):
    station_id = str(request.GET.get('id'))
    station_data_temp = get_station_data(station_id)
    if not station_data_temp:
        return JsonResponse({'error': '정류소 데이터를 찾을 수 없습니다.'}, status=404)
    station = station_data_temp[0]
    # 주차된 따릉이 대수: station_data['parkingBikeTotCnt']
    return render(request, 'stations/station_info.html', {'station': station})


def stations_data(request):
    stations = get_all_stations_data()
    return render(request, 'stations/station_list.html', {'stations': stations})
