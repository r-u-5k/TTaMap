from django.http import JsonResponse
from .services import fetch_public_transport_path

def get_path(request):
    try:
        data = fetch_public_transport_path()
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
