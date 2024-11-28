from django.urls import path, include
from . import views

urlpatterns = [
    path('near-stations', views.near_stations_view, name='near-stations'),
    path('data', views.station_data_view, name='get-station-data'),
    path('data/all', views.all_stations_data_view, name='get-all-stations'),
]
