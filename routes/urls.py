from django.urls import path, include
from . import views

urlpatterns = [
    path('odsay', views.odsay_route_view, name="odsay_route"),
    path('walk', views.walk_route_view, name="walk_route"),
    path('bike', views.bike_route_view, name="bike_route"),
    path('full', views.full_route_view, name="full_route"),
    path('simple', views.simple_route_view, name="simple_route"),
]
