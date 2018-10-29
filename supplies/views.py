from django.shortcuts import render
from django.http import HttpResponse

from home.models import Category, Item

def index(request):
    if "cart" not in request.session:
        request.session["cart"] = []
    if request.method == 'POST':
        item_id = request.POST.get('itemID')
        quantity = request.POST.get('quantity')
        print(request.session["cart"])
        #if item_id not in request.session["cart"]:
            #request.session["cart"][item_id] = 0
            #print('waqas')
        request.session["cart"].append(([item_id],int(quantity)))
    print(request.session["cart"])
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

