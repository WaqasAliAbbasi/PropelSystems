from django.shortcuts import render
from django.http import HttpResponse

from home.models import Clinic, Category, Item, Order, OrderItem

import json

def index(request):
    try:
        category_id = request.GET.get('category_id', Category.objects.first().id)
        category = Category.objects.get(pk=category_id)
    except:
        category = Category.objects.first()
    items = Item.objects.filter(category=category)
    context = {
        'category_id': category.id,
        'categories': Category.objects.all(),
        'items': items
    }
    return render(request, 'supplies/index.html', context)

def add_to_cart(request):
    if "cart" not in request.session:
        request.session["cart"] = {
            "items": {}
        }
    if request.method == 'POST':
        item_id = request.POST.get('itemID')
        quantity = request.POST.get('quantity')
        if item_id not in request.session["cart"]["items"]:
            request.session["cart"]["items"][item_id] = 0
        request.session["cart"]["items"][item_id] += int(quantity)
        request.session.modified = True
    return HttpResponse("Successfully added to cart: " + json.dumps(request.session["cart"]))

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

    

