from django.db import models

class Warehouse(models.Model):
    name = models.CharField(max_length=200)

class Category(models.Model):
    name = models.CharField(max_length=200)

class Item(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    shipping_weight_grams = models.PositiveIntegerField()

class Clinic(models.Model):
    name = models.CharField(max_length=200)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    altitude_meters = models.PositiveIntegerField()

class Order(models.Model):
    QUEUED_FOR_PROCESSING = 1
    PROCESSING_BY_WAREHOUSE = 2
    QUEUED_FOR_DISPATCH = 3
    DISPATCHED = 4
    DELIVERED = 5
    status = models.IntegerField(choices=((QUEUED_FOR_PROCESSING ,'Queued for Processing'), (PROCESSING_BY_WAREHOUSE,'Processing by Warehouse'), (QUEUED_FOR_DISPATCH,'Queued for Dispatch'), (DISPATCHED,'Dispatched'), (DELIVERED,'Delivered')), default=1)
    priority = models.IntegerField(choices=((1,'Low'),(2,'Medium'),(3,'High')), default=2)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    time_placed = models.DateTimeField(auto_now_add=True, blank=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
