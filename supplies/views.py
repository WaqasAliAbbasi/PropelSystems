from django.shortcuts import render
from django.http import HttpResponse

from .models import Item

def index(request):
    supplies_list = Item.objects.all()
    context = {
        'supplies_list': supplies_list,
    }
    return render(request, 'supplies/index.html', context)
