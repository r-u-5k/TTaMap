from django.urls import path, include
from . import views

urlpatterns = [
    path('near-stations/', views.get_near_stations, name='near_stations'),
]
