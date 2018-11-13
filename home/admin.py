from django.contrib import admin

from .models import Location, Distance, Warehouse, Category, Item, Order, OrderItem, Clinic

class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('time_placed','time_dispatched',)

admin.site.register(Location)
admin.site.register(Distance)
admin.site.register(Warehouse)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Clinic)
