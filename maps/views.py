import requests
from django.shortcuts import render
from django.http import JsonResponse
import params as pa
from .services import get_all_stations_data


def map_view(request):
    return render(request, 'maps/map.html')

def stations_data(request):
    stations = get_all_stations_data()
    # HTML 템플릿에 전달
    return JsonResponse({'stations': stations})
