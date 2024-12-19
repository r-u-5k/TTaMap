from django.http import JsonResponse
from django.shortcuts import render

from .services import get_odsay_route, get_full_route, get_bike_route, get_walk_route, get_simple_route


# Create your views here.
def odsay_route_view(request):
    start_lat = request.GET.get('slat')
    start_lng = request.GET.get('slng')
    end_lat = request.GET.get('elat')
    end_lng = request.GET.get('elng')
    try:
        data = get_odsay_route(start_lat, start_lng, end_lat, end_lng)
        if data['result']['path'][0]['subPath'][0]['trafficType'] == 3:
            print(f"출발지에서 대중교통 탑승 전까지 도보 이동 거리: {data['result']['path'][0]['subPath'][0]['distance']}m")
            print(f"출발지에서 대중교통 탑승 전까지 도보 이동 시간: {data['result']['path'][0]['subPath'][0]['sectionTime']}분")
        if data['result']['path'][0]['subPath'][-1]['trafficType'] == 3:
            print(f"대중교통 하차 후 목적지까지 도보 이동 거리: {data['result']['path'][0]['subPath'][-1]['distance']}m")
            print(f"대중교통 하차 후 목적지까지 도보 이동 시간: {data['result']['path'][0]['subPath'][-1]['sectionTime']}분")

        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def walk_route_view(request):
    start_lat = request.GET.get('slat')
    start_lng = request.GET.get('slng')
    end_lat = request.GET.get('elat')
    end_lng = request.GET.get('elng')
    try:
        data = get_walk_route(start_lat, start_lng, end_lat, end_lng)
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def bike_route_view(request):
    start_lat = request.GET.get('slat')
    start_lng = request.GET.get('slng')
    end_lat = request.GET.get('elat')
    end_lng = request.GET.get('elng')
    try:
        data = get_bike_route(start_lat, start_lng, end_lat, end_lng)
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def full_route_view(request):
    start_lat = request.GET.get('slat')
    start_lng = request.GET.get('slng')
    end_lat = request.GET.get('elat')
    end_lng = request.GET.get('elng')
    try:
        data = get_full_route(start_lat, start_lng, end_lat, end_lng)
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def simple_route_view(request):
    start_lat = request.GET.get('slat')
    start_lng = request.GET.get('slng')
    end_lat = request.GET.get('elat')
    end_lng = request.GET.get('elng')
    try:
        data = get_simple_route(start_lat, start_lng, end_lat, end_lng)
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def route_view(request):
    return render(request, 'routes/route.html')
