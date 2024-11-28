from django.urls import path, include
from . import views

urlpatterns = [
    path('near-stations', views.view_near_stations, name='near-stations'),
    path('data', views.view_station_data, name='get-station-data'),
    path('data/all', views.view_all_stations_data, name='get-all-stations'),
]
