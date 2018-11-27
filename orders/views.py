from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from home.decorators import clinic_manager_required
from home.views import access
from home.models import Order

import datetime

@login_required
@clinic_manager_required
def orders(request):
    orders = Order.objects.filter(clinic=request.user.clinic).exclude(status=Order.DELIVERED).exclude(status=Order.CANCELLED).order_by('time_placed')
    context = {
        'sidebar': access[request.user.role],
        'user': request.user,
        'location': request.user.clinic.name,
        'orders': orders
    }
    return render(request, 'orders/index.html', context)

def notify_delivery(request):
    if request.method == 'POST':
        order_id = request.POST.get('orderID')
        order = Order.objects.get(id=order_id)
        if order.status != Order.DISPATCHED:
            return HttpResponse("Error: Undispatched order #" + str(order_id) + " cannot be classified as delivered.")
        order.status = Order.DELIVERED
        order.time_delivered = datetime.datetime.now()
        order.save()
        return HttpResponse("Successfully classified order #" + str(order_id) + " as delivered.")

def cancel(request):
    if request.method == 'POST':
        order_id = request.POST.get('orderID')
        order = Order.objects.get(id=order_id)
        if order.status != Order.QUEUED_FOR_PROCESSING:
            return HttpResponse("Error: Order #" + str(order_id) + " cannot be cancelled at this point.")
        order.status = Order.CANCELLED
        order.save()
        return HttpResponse("Successfully classified order #" + str(order_id) + " as cancelled.")
