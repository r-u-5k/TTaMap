from django.urls import path, include
from .views import near_stations_view, all_stations_data_view, station_data_view

urlpatterns = [
    path('near', near_stations_view, name='near_stations'),
    path('data/all', all_stations_data_view, name='all_stations'),
    path('data', station_data_view, name='station_data')
]
