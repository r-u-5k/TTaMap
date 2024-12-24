from django.urls import path, include
from . import views

app_name = 'routes'
urlpatterns = [
    path('api/odsay', views.odsay_route_view, name="odsay_route"),
    path('api/walk', views.walk_route_view, name="walk_route"),
    path('api/bike', views.bike_route_view, name="bike_route"),
    path('api/full', views.full_route_view, name="full_route"),
    path('api/simple', views.simple_route_view, name="simple_route"),
    path('', views.route_view, name="route"),
    path('result/', views.route_result_view, name="route_result"),
]
