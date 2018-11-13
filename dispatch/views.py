import csv
import itertools
import datetime
from django.shortcuts import render
from django.http import HttpResponse
from home.models import Distance, Warehouse, Clinic, Order

DRONE_LOAD_CARRYING_CAPACITY = 25 * 1000
ORDER_OVERHEAD_WEIGHT = 1.2 * 1000

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
    for b in route:
        d = 0
        try:
            d = Distance.objects.get(location_from=a,location_to=b)
        except:
            try:
                d = Distance.objects.get(location_from=b,location_to=a)
            except:
                return -1000
        distance += d
        a = b
    return distance

def get_itinerary(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;'

    writer = csv.writer(response)
    writer.writerow(['Location', 'Latitude', 'Longitude', 'Altitude'])

    starting_point = Warehouse.objects.first()

    clinics_high = set()
    clinics_medium = set()
    clinics_low = set()
    for order in get_current_shipment():
        if order.priority == Order.HIGH:
            clinics_high.add(order.clinic)
        elif order.priority == Order.MEDIUM:
            if order.clinic not in clinics_high:
                clinics_medium.add(order.clinic)
        else:
            if order.clinic not in clinics_high and order.clinic not in clinics_low:
                clinics_low.add(order.clinic)
    
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
    
    # Add starting point at end of csv as required
    best_route += [starting_point]
    # Write itinerary to csv
    for location in best_route:
        writer.writerow([location.name, location.latitude, location.longitude, location.altitude_meters])

    return response
