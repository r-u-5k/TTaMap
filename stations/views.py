from django.http import JsonResponse

from .services import *


def get_near_stations(request):
    latitude = float(request.GET.get('lat'))
    longitude = float(request.GET.get('lng'))
    nearby_stations = fetch_near_stations(latitude, longitude)
    return JsonResponse({'stations': nearby_stations})


def get_station_data(request):
    station_id = str(request.GET.get('id'))
    station_data = fetch_station_data(station_id)[0]
    return JsonResponse(station_data, safe=False)
