from django.contrib import admin
from django.urls import path, include
from .views import index, signin, signup, verify, verifyCode, result


urlpatterns = [
    path('', index, name="main_index"),
    path('signup', signup, name='main_signup'),
    path('signin', signin, name='main_signin'),
    path('verifyCode', verifyCode, name='main_verifyCode'),
    path('verify', verify, name='main_verify'),
    path('result', result, name='main_result'),
]
