from django.contrib import admin
from django.urls import path, include
from .views import caculate


urlpatterns = [
    path('send', calculate, name="calculate_do"),
    
]
