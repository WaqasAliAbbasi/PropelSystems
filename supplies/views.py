import copy
from django.shortcuts import render
from django.http import HttpResponse
from home.models import Clinic, Category, Item, Order, OrderItem
from dispatch.views import DRONE_LOAD_CARRYING_CAPACITY, ORDER_OVERHEAD_WEIGHT
from django.contrib.auth.decorators import login_required
from home.decorators import clinic_manager_required
from home.views import access
import json

@login_required
@clinic_manager_required
def supplies(request):
    try:
        # Check if category id specified in the URL
        category_id = request.GET.get('category_id')
        category = Category.objects.get(pk=category_id)
    except:
        # Default to first category if category id not specified or invalid
        category = Category.objects.first()
    items = Item.objects.filter(warehouse=request.user.clinic.linked_warehouse, category=category)
    context = {
        'sidebar': access[request.user.role],
        'name': request.user.get_full_name(),
        'role': request.user.get_role_display,
        'location': request.user.clinic.name,
        'category_id': category.id,
        'categories': Category.objects.all(),
        'items': items
    }
    return render(request, 'supplies/index.html', context)

def get_cart_weight(items):
    cart_weight = ORDER_OVERHEAD_WEIGHT
    for item in items:
        cart_weight += Item.objects.get(pk=item).shipping_weight_grams * items[item]
    return cart_weight

def add_to_cart(request):
    if request.method == 'POST':
        # request.session["cart"]["items"] is a dictionary of item_id -> quantity
        if "cart" not in request.session:
            request.session["cart"] = {
                "items": {}
            }

        item_id = request.POST.get('itemID')
        quantity = request.POST.get('quantity')

        # Deep copy the cart from session so we don't affect it if the new cart is invalid
        items = copy.deepcopy(request.session["cart"]["items"])

        # Check if the item already exists in cart
        if item_id not in items:
            items[item_id] = 0

        # Increase quantity of item in cart
        items[item_id] += int(quantity)

        cart_weight = get_cart_weight(items)

        # If new cart is invalid, return error and don't affect cart in session
        if cart_weight > DRONE_LOAD_CARRYING_CAPACITY:
            return HttpResponse("Unable to add item to cart as it will exceed the drone's carrying capacity by " + str((cart_weight - DRONE_LOAD_CARRYING_CAPACITY)/1000) + " kg.")

        # If new cart valid, save it to session
        request.session["cart"]["items"] = copy.deepcopy(items)
        request.session.modified = True

        return HttpResponse("Successfully added to cart.  Weight: " + str(cart_weight/1000) + "/" + str(DRONE_LOAD_CARRYING_CAPACITY/1000) + " kg.")

def flush_session(request):
    request.session.flush()
    return HttpResponse("Session flushed.")

@login_required
@clinic_manager_required
def cart(request):
    cart_items = []
    # request.session["cart"]["items"] is a dictionary of item_id -> quantity
    if "cart" in request.session and "items" in request.session["cart"]:
        for item_id in request.session["cart"]["items"]:
            quantity = request.session["cart"]["items"][item_id]
            cart_items.append({
                "item": Item.objects.get(pk=item_id),
                "quantity": quantity
            })
    context = {
        'sidebar': access[request.user.role],
        'name': request.user.get_full_name(),
        'location': request.user.clinic.name,
        'role': request.user.get_role_display,
        'cart_items': cart_items
    }
    return render(request, 'cart/index.html', context)

def checkout(request):
    if request.method == 'POST':
        if not request.session["cart"] or not request.session["cart"]["items"]:
            return HttpResponse("No items in cart.")
        new_order = Order(status = Order.QUEUED_FOR_PROCESSING, priority = request.POST.get('priority'), clinic = request.user.clinic)
        new_order.save()
        for item_id in request.session["cart"]["items"]:
            quantity = request.session["cart"]["items"][item_id]
            oi = OrderItem(order=new_order, item=Item.objects.get(pk=item_id), quantity=quantity)
            oi.save()
        # Empty the session
        request.session["cart"] = {
            "items": {}
        }
        return HttpResponse("Successfully created order.")
