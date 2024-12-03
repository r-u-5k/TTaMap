from django.urls import path, include
from . import views

urlpatterns = [
    path('pt', views.pt_route_view, name="public_transport_route"),
]
