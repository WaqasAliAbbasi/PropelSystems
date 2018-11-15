from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from .models import User, Location, Distance, Warehouse, Category, Item, Order, OrderItem, Clinic

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    list_display = UserAdmin.list_display + ('role', 'location')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role','location',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role','location',)}),
    )

class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('time_placed','time_dispatched',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Location)
admin.site.register(Distance)
admin.site.register(Warehouse)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Clinic)