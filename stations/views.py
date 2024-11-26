from django.http import JsonResponse

from .services import *


def get_near_stations(request):
    latitude = float(request.GET.get('lat'))
    longitude = float(request.GET.get('lng'))
    nearby_stations = get_nearby_stations(latitude, longitude)
    return JsonResponse({'stations': nearby_stations})
