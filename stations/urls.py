from django.urls import path, include
from .views import *

urlpatterns = [
    path('near', near_stations_view, name='near'),
    path('data', station_data_view, name='station-data'),
    path('data/all', all_stations_data_view, name='all-stations-data'),
]
