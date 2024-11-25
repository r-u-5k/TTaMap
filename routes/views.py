from django.shortcuts import render
from django.http import JsonResponse
from .services import fetch_public_transport_route

# Create your views here.
def get_route(request):
    try:
        data = fetch_public_transport_route()
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
