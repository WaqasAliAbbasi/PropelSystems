import copy
from django.shortcuts import render
from django.http import HttpResponse

from home.models import Clinic, Category, Item, Order, OrderItem
from dispatch.views import DRONE_LOAD_CARRYING_CAPACITY, ORDER_OVERHEAD_WEIGHT

import json

def index(request):
    try:
        category_id = request.GET.get('category_id', Category.objects.first().id)
        category = Category.objects.get(pk=category_id)
    except:
        category = Category.objects.first()
    items = Item.objects.filter(category=category)
    context = {
        'location': Clinic.objects.first().name,
        'role': "Clinic Manager",
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
    if "cart" not in request.session:
        request.session["cart"] = {
            "items": {}
        }
    if request.method == 'POST':
        item_id = request.POST.get('itemID')
        quantity = request.POST.get('quantity')

        items = copy.deepcopy(request.session["cart"]["items"])
        if item_id not in items:
            items[item_id] = 0
        items[item_id] += int(quantity)

        cart_weight = get_cart_weight(items)
        if cart_weight > DRONE_LOAD_CARRYING_CAPACITY:
            return HttpResponse("Unable to add item to cart as it will exceed the drone's carrying capacity by " + str((cart_weight - DRONE_LOAD_CARRYING_CAPACITY)/1000) + " kg.")

        request.session["cart"]["items"] = copy.deepcopy(items)
        request.session.modified = True

        return HttpResponse("Successfully added to cart.  Weight: " + str(cart_weight/1000) + "/" + str(DRONE_LOAD_CARRYING_CAPACITY/1000) + " kg.")

def flush_session(request):
    request.session.flush()
    return HttpResponse("Session flushed.")

def cart(request):
    if "cart" not in request.session:
        request.session["cart"] = {
            "items": {}
        }
    cart_items = []
    for item in request.session["cart"]["items"]:
        cart_items.append({
            "item": Item.objects.get(pk=item),
            "quantity": request.session["cart"]["items"][item]
        })
    context = {
        'location': Clinic.objects.first().name,
        'role': "Clinic Manager",
        'cart_items': cart_items
    }
    return render(request, 'cart/index.html', context)

def checkout(request):
    if request.method == 'POST':
        if "cart" not in request.session:
            request.session["cart"] = {
                "items": {}
            }
            return HttpResponse("No items in cart.")
        if not request.session["cart"]["items"]:
            return HttpResponse("No items in cart.")
        new_order = Order()
        new_order.status = 1
        new_order.priority = request.POST.get('priority')
        new_order.clinic = Clinic.objects.first()
        new_order.save()
        cart_items = []
        for item in request.session["cart"]["items"]:
            oi = OrderItem(order=new_order, item=Item.objects.get(pk=item), quantity=request.session["cart"]["items"][item])
            oi.save()
        request.session["cart"] = {
            "items": {}
        }
        return HttpResponse("Successfully created order.")
