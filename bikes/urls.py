from django.urls import path, include
from . import views

urlpatterns = [
    path('test/', views.get_api, name='path'),
]