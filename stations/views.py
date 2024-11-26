from django.http import JsonResponse

from .services import *


def get_near_stations(request):
    latitude = float(request.GET.get('lat'))
    longitude = float(request.GET.get('lng'))
    nearby_stations = get_nearby_stations(latitude, longitude)
    return JsonResponse({'stations': nearby_stations})


def get_station_data(request):
    station_id = request.GET.get('station_id')
    station_data = get_station_data(station_id)
    return JsonResponse(station_data)
