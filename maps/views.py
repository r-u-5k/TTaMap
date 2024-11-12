from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def main(request):
    message = request.GET.get('message')
    print(message)

    return HttpResponse("Hello")