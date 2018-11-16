import itertools
import datetime
import io
from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from home.models import Distance, Warehouse, Clinic, Order, OrderItem, Item
from django.contrib.auth.decorators import login_required
from home.decorators import warehouse_personnel_required
from home.urls import access
from reportlab.pdfgen import canvas

def get_queued():
    orders = Order.objects.filter(status=Order.QUEUED_FOR_PROCESSING).order_by('-priority','time_placed')
    return orders

def get_processing():
    orders = Order.objects.filter(status=Order.PROCESSING_BY_WAREHOUSE).order_by('-priority','time_placed')
    return orders

def get_details(order_id):
    order = Order.objects.filter(id=order_id)[0]
    orderitems = OrderItem.objects.filter(order=order)
    return orderitems

def get_order_by_id(order_id):
    order = Order.objects.filter(id=order_id)[0]
    return order

@login_required
@warehouse_personnel_required
def warehouse(request):
    queued = get_queued()
    processing = get_processing()
    context = {
        'sidebar': access[request.user.role],
        'name': request.user.get_full_name(),
        'role': request.user.get_role_display,
        'queued': queued,
        'processing': processing
    }
    if request.user.location:
        context['location'] = request.user.location.name
    return render(request, 'warehouse/index.html', context)

def process_next_order(request):
    # if request.method == 'POST':
    #     processing = get_processing()
    #     if not processing:
    #         return HttpResponse("No orders in queue.")
    #     for order in processing:
    #         order.status = Order.QUEUED_FOR_PROCESSING
    #         order.save()
    #     return HttpResponse("Moved order to processing.")
    if request.method == 'POST':
        queued = get_queued()
        if not queued:
            return HttpResponse("No orders in queue.")
        else:
            queued[0].status = Order.PROCESSING_BY_WAREHOUSE
            queued[0].save()
        return HttpResponse("Moved order to processing.")

def view_order_details(request):
    if request.method == 'POST':
        order_id = request.POST['order_id']
        orderitems = get_details(order_id)
        text = ""
        for orderitem in orderitems:
            text += (OrderItem.orderitem_details(orderitem)) + '\n'
        return HttpResponse(text)

def get_order_label(request):
    if request.method == 'GET':
        order_id = request.GET['order_id']
        order = get_order_by_id(order_id)
        orderitems = get_details(order_id)

        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment;filename="shipping_label.pdf"'

        # Create the PDF object, using the response object as its "file."
        p = canvas.Canvas(response)

        p.drawString(100, 750, "Order ID: " + str(order_id))
        p.drawString(100, 700, "Order Destination: " + str(order.clinic.name))
        p.drawString(100, 650, "Order Contents: ")
        count = 1
        for orderitem in orderitems:
            p.drawString(100, 650 - (count * 25), OrderItem.orderitem_details(orderitem))
            count += 1
        p.save()

        return response

def move_to_dispatch(request):
    if request.method == 'POST':
        order_id = request.POST['order_id']
        processing = get_processing()
        for order in processing:
            if str(order.id) == str(order_id):
                order.status = Order.QUEUED_FOR_DISPATCH
                order.save()
                return HttpResponse("Moved order to dispatch queue")

        return HttpResponse("Error: Order cannot be found.")
