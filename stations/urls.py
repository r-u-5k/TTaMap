from django.urls import path, include
from . import views

urlpatterns = [
    path('near/', views.get_near_stations, name='near'),
]
