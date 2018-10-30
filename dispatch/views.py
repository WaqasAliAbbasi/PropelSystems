import csv
from heapq import heappush, heappop
from django.shortcuts import render
from django.http import HttpResponse
from home.models import Order

DRONE_LOAD_CARRYING_CAPACITY = 25 * 1000
ORDER_OVERHEAD_WEIGHT = 1.2 * 1000
distance_dict={
    'Mui Wo General Out-patient Clinic': [('North Lamma General Out-patient Clinic',12.54),
    ('Peng Chau General Out-patient Clinic',4.68),
    ('Sok Kwu Wan General Out-patient Clinic', 15.32),
    ('Tai O General Out-patient Clinic', 14.44),
    ('Aberdeen General Out-patient Clinic', 16.41),
    ('Ap Lei Chau General Out-patient Clinic', 16.24),
    ('Queen Mary Hospital Drone Port', 13.74)],
    'North Lamma General Out-patient Clinic':[('Peng Chau General Out-patient Clinic', 9.92),
    ('Sok Kwu Wan General Out-patient Clinic',2.96),
    ('Tai O General Out-patient Clinic', 26.29),
    ('Aberdeen General Out-patient Clinic', 5.45),
    ('Ap Lei Chau General Out-patient Clinic', 4.87),
    ('Queen Mary Hospital Drone Port', 5.52)],
    'Peng Chau General Out-patient Clinic':[('Sok Kwu Wan General Out-patient Clinic', 12.88),
    ('Tai O General Out-patient Clinic', 18.90),
    ('Aberdeen General Out-patient Clinic', 12.64),
    ('Ap Lei Chau General Out-patient Clinic', 12.62),
    ('Queen Mary Hospital Drone Port', 9.61)],
    'Sok Kwu Wan General Out-patient Clinic':[('Tai O General Out-patient Clinic', 28.71),
    ('Aberdeen General Out-patient Clinic', 5.53),
    ('Ap Lei Chau General Out-patient Clinic', 4.77),
    ('Queen Mary Hospital Drone Port', 7.19)],
    'Tai O General Out-patient Clinic':[('Aberdeen General Out-patient Clinic',30.72),
    ('Ap Lei Chau General Out-patient Clinic',30.47),
    ('Queen Mary Hospital Drone Port',28.18)],
    'Aberdeen General Out-patient Clinic':[('Ap Lei Chau General Out-patient Clinic',0.77),
    ('Queen Mary Hospital Drone Port',3.44)],
    'Ap Lei Chau General Out-patient Clinic':[('Queen Mary Hospital Drone Port',3.79)]
}


def ucsGsa(stateSpaceGraph, startState, goalState): 
    frontier = []
    heappush(frontier, (0, [startState]))
    exploredSet = set()
    print('Initial frontier:',list(frontier))
    while frontier:
        node = heappop(frontier)
        if (node[1] == goalState): return node
        if node[1][-1] not in exploredSet:
            print('Exploring:',node[1][-1],'at cost',node[0])
            exploredSet.add(node[1][-1])
            for child in stateSpaceGraph[node[1][-1]]:
                heappush(frontier, (node[0]+child[0], node[1]+child[1]))
            print(list(frontier))
            print(exploredSet)

def ucs_search(orders):
    routes = []
    for order in orders:
        routes.append(ucsGsa(distance_dict, order, 'Queen Mary Hospital Drone Port'))
    min_val = routes[0][0]
    final_route = routes[0][1]
    for route in routes:
        if route[0] < min_val:
            min_val = route[0]
            final_route = route[1]
    return final_route


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
        'items': current_shipment
    }
    return render(request, 'dispatch/index.html', context)

def dispatch_shipment(request):
    if request.method == 'POST':
        current_shipment = get_current_shipment()
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
