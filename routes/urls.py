from django.urls import path, include
from . import views

urlpatterns = [
    path('pt', views.pt_route_view, name="public_transport_route"),
    path('full', views.route_view, name="full_route"),
    path('html', views.route_html_view, name='route_html')
]
