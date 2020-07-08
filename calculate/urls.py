from django.contrib import admin
from django.urls import path, include
from .views import calculate


urlpatterns = [
    path('', calculate, name="calculate_do"),
    
]
