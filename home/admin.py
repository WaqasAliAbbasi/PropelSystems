from django.contrib import admin

from .models import Warehouse, Category, Item, Order, OrderItem, Clinic

admin.site.register(Warehouse)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Clinic)
