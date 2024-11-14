from django.http import JsonResponse

from .services import fetch_bikes


# Create your views here.
def get_api(request):
    try:
        data = fetch_bikes()
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
