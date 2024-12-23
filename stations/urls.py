from django.urls import path, include
from .views import near_stations_view, station_list_view

app_name = 'stations'
urlpatterns = [
    path('api/near', near_stations_view, name='near_stations'),
    path('list', station_list_view, name='station_list'),
]
