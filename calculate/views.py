from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def caculate(request):
    return HttpResponse("Calculate, calculate function!")