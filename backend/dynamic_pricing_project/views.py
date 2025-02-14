from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse('<h3>Dynamic Pricing Algo API. <br><br><br> See <a href="/swagger"> swagger documentation here</a>.<h3>')

