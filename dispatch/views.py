import csv
from django.shortcuts import render
from django.http import HttpResponse
from home.models import Warehouse, Order

DRONE_LOAD_CARRYING_CAPACITY = 25 * 1000
ORDER_OVERHEAD_WEIGHT = 1.2 * 1000
distance_dict={
    'Mui Wo Clinic': [('North Lamma Clinic',12.54),
    ('Peng Chau Clinic',4.68),
    ('Sok Kwu Wan Clinic', 15.32),
    ('Tai O Clinic', 14.44),
    ('Aberdeen Clinic', 16.41),
    ('Ap Lei Chau Clinic', 16.24),
    ('Queen Mary Hospital', 13.74)],
    'North Lamma Clinic':[('Peng Chau Clinic', 9.92),
    ('Sok Kwu Wan Clinic',2.96),
    ('Tai O Clinic', 26.29),
    ('Aberdeen Clinic', 5.45),
    ('Ap Lei Chau Clinic', 4.87),
    ('Queen Mary Hospital', 5.52)],
    'Peng Chau Clinic':[('Sok Kwu Wan Clinic', 12.88),
    ('Tai O Clinic', 18.90),
    ('Aberdeen Clinic', 12.64),
    ('Ap Lei Chau Clinic', 12.62),
    ('Queen Mary Hospital', 9.61)],
    'Sok Kwu Wan Clinic':[('Tai O Clinic', 28.71),
    ('Aberdeen Clinic', 5.53),
    ('Ap Lei Chau Clinic', 4.77),
    ('Queen Mary Hospital', 7.19)],
    'Tai O Clinic':[('Aberdeen Clinic',30.72),
    ('Ap Lei Chau Clinic',30.47),
    ('Queen Mary Hospital',28.18)],
    'Aberdeen Clinic':[('Ap Lei Chau Clinic',0.77),
    ('Queen Mary Hospital',3.44)],
    'Ap Lei Chau Clinic':[('Queen Mary Hospital',3.79)]
}

def get_current_shipment():
    orders = Order.objects.filter(status=Order.QUEUED_FOR_DISPATCH)
    current_shipment = []
    remaining_weight = DRONE_LOAD_CARRYING_CAPACITY
    for order in orders:
        order_weight = ORDER_OVERHEAD_WEIGHT
        for order_item in order.orderitem_set.all():
            order_weight += order_item.quantity * order_item.item.shipping_weight_grams
        if order_weight < remaining_weight:
            remaining_weight -= order_weight
            current_shipment.append(order)
        else:
            break
    return current_shipment

def index(request):
    current_shipment = get_current_shipment()
    context = {
        'location': Warehouse.objects.first().name,
        'role': "Dispatcher",
        'items': current_shipment
    }
    return render(request, 'dispatch/index.html', context)

def dispatch_shipment(request):
    if request.method == 'POST':
        current_shipment = get_current_shipment()
        if not current_shipment:
            return HttpResponse("No shipment found.")
        for order in current_shipment:
            order.status = Order.DISPATCHED
            order.save()
        return HttpResponse("Successfully dispatched shipments.")

def get_itinerary(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;'

    writer = csv.writer(response)
    writer.writerow(['Location', 'Latitude', 'Longitude', 'Altitude'])

    current_shipment = get_current_shipment()
    for order in current_shipment:
        writer.writerow([order.clinic.name, order.clinic.latitude, order.clinic.longitude, order.clinic.altitude_meters])

    return response
