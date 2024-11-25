from django.http import HttpResponseRedirect

def map_view(request):
    return HttpResponseRedirect('http://localhost:3000/map/')
