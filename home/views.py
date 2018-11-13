from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse(
        "<h1>AS-P Homepage</h1><ul><li><a href='/supplies'>Supplies</a></li><li><a href='/dispatch'>Dispatch</a></li></ul>"
    )
