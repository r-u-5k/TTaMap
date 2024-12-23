from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.map_view, name='map'),
    path('api/station', views.station_data_view, name='station_data'),
    path('api/stations', views.stations_data, name='stations_data'),
]
