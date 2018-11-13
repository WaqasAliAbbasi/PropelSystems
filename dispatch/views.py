import csv
import itertools
import datetime
from heapq import heappush, heappop
from django.shortcuts import render
from django.http import HttpResponse
from home.models import Warehouse, Clinic, Order

DRONE_LOAD_CARRYING_CAPACITY = 25 * 1000
ORDER_OVERHEAD_WEIGHT = 1.2 * 1000

external_data = {
  "Mui Wo General Out-patient Clinic": [
    ("North Lamma General Out-patient Clinic", 12.54),
    ("Peng Chau General Out-patient Clinic", 4.68),
    ("Sok Kwu Wan General Out-patient Clinic", 15.32),
    ("Tai O Jockey Club General Out-patient Clinic", 14.44),
    ("Aberdeen General Out-patient Clinic", 16.41),
    ("Ap Lei Chau General Out-patient Clinic", 16.24),
    ("Queen Mary Hospital Drone Port", 13.74)
  ],
  "North Lamma General Out-patient Clinic": [
    ("Peng Chau General Out-patient Clinic", 9.92),
    ("Sok Kwu Wan General Out-patient Clinic", 2.96),
    ("Tai O Jockey Club General Out-patient Clinic", 26.29),
    ("Aberdeen General Out-patient Clinic", 5.45),
    ("Ap Lei Chau General Out-patient Clinic", 4.87),
    ("Queen Mary Hospital Drone Port", 5.52)
  ],
  "Peng Chau General Out-patient Clinic": [
    ("Sok Kwu Wan General Out-patient Clinic", 12.88),
    ("Tai O Jockey Club General Out-patient Clinic", 18.9),
    ("Aberdeen General Out-patient Clinic", 12.64),
    ("Ap Lei Chau General Out-patient Clinic", 12.62),
    ("Queen Mary Hospital Drone Port", 9.61)
  ],
  "Sok Kwu Wan General Out-patient Clinic": [
    ("Tai O Jockey Club General Out-patient Clinic", 28.71),
    ("Aberdeen General Out-patient Clinic", 5.53),
    ("Ap Lei Chau General Out-patient Clinic", 4.77),
    ("Queen Mary Hospital Drone Port", 7.19)
  ],
  "Tai O Jockey Club General Out-patient Clinic": [
    ("Aberdeen General Out-patient Clinic", 30.72),
    ("Ap Lei Chau General Out-patient Clinic", 30.47),
    ("Queen Mary Hospital Drone Port", 28.18)
  ],
  "Aberdeen General Out-patient Clinic": [
    ("Ap Lei Chau General Out-patient Clinic", 0.77),
    ("Queen Mary Hospital Drone Port", 3.44)
  ],
  "Ap Lei Chau General Out-patient Clinic": [
    ("Queen Mary Hospital Drone Port", 3.79)
  ]
}
distance_dict = {}
for a in external_data:
    if not a in distance_dict:
        distance_dict[a] = {}
    for b in external_data[a]:
        distance_dict[a][b[0]] = b[1]
        if not b[0] in distance_dict:
            distance_dict[b[0]] = {}
        distance_dict[b[0]][a] = b[1]

def ucsGsa(stateSpaceGraph, startState, goalState):
    frontier = []
    heappush(frontier, (0, [startState]))
    exploredSet = set()
    while frontier:
        node = heappop(frontier)
        if (node[1] == goalState): return node
        if node[1][-1] not in exploredSet:
            exploredSet.add(node[1][-1])
            for child in stateSpaceGraph[node[1][-1]]:
                heappush(frontier, (node[0]+child[0], node[1]+child[1]))

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

# get_current_shipment gets all orders for the current valid shipment
def get_current_shipment():
    # Get all orders ordered by priority and then time placed
    orders = Order.objects.filter(status=Order.QUEUED_FOR_DISPATCH).order_by('-priority','time_placed')
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

def dispatch(request):
    current_shipment = get_current_shipment()
    context = {
        'location': Warehouse.objects.first().name,
        'role': "Dispatcher",
        'orders': current_shipment
    }
    return render(request, 'dispatch/index.html', context)

def dispatch_shipment(request):
    if request.method == 'POST':
        current_shipment = get_current_shipment()
        if not current_shipment:
            return HttpResponse("No shipment found.")
        for order in current_shipment:
            order.status = Order.DISPATCHED
            order.time_dispatched = datetime.datetime.now()
            order.save()
        return HttpResponse("Successfully dispatched shipments.")

def get_distance(route):
    distance = 0
    a = route[0]
    for b in route[1:]:
        if b not in distance_dict[a]:
            return -1000
        distance += distance_dict[a][b]
        a = b
    return distance

def get_itinerary(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;'

    writer = csv.writer(response)
    writer.writerow(['Location', 'Latitude', 'Longitude', 'Altitude'])

    starting_point = Warehouse.objects.first().name

    clinics_high = set()
    clinics_medium = set()
    clinics_low = set()
    for order in get_current_shipment():
        if order.priority == Order.HIGH:
            clinics_high.add(order.clinic.name)
        elif order.priority == Order.MEDIUM:
            if order.clinic.name not in clinics_high:
                clinics_medium.add(order.clinic.name)
        else:
            if order.clinic.name not in clinics_high and order.clinic.name not in clinics_low:
                clinics_low.add(order.clinic.name)
    
    # permutations of each priority category
    permutations_clinics_high = [list(x) for x in itertools.permutations(list(clinics_high))]
    permutations_clinics_medium = [list(x) for x in itertools.permutations(list(clinics_medium))]
    permutations_clinics_low = [list(x) for x in itertools.permutations(list(clinics_low))]
    
    # product of all the permutations for each category leading from high to medium to low
    possible_routes = list(itertools.product(permutations_clinics_high,permutations_clinics_medium,permutations_clinics_low))
    for i in range(len(possible_routes)):
        possible_routes[i] = possible_routes[i][0] + possible_routes[i][1] + possible_routes[i][2]

    # Start off with the first route as the best
    best_route = possible_routes[0]
    # Add warehouse at start and end
    minimum_distance = get_distance([starting_point] + best_route + [starting_point])
    # Check all other routes
    for possible_route in possible_routes[1:]:
        route = possible_route
        # Add warehouse at start and end
        distance = get_distance([starting_point] + route  + [starting_point])
        if distance < minimum_distance:
            minimum_distance = distance
            best_route = route

    final_route = []
    for clinic in best_route:
        final_route.append(Clinic.objects.get(name=clinic))
    # Add warehouse at end of final route as per requirement
    final_route += [Warehouse.objects.get(name=starting_point)]

    # Write itinerary to csv
    for stop in final_route:
        writer.writerow([stop.name, stop.latitude, stop.longitude, stop.altitude_meters])

    return response
