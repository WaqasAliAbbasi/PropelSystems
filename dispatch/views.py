from django.shortcuts import render
from django.http import HttpResponse

from home.models import Order

# Create your views here.

def index(request):
    orders = Order.objects.all()
    context = {
        'items': orders
    }
    return render(request, 'dispatch/index.html', context)
