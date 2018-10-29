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

class Order(models.Model):
    status = models.IntegerField(choices=((1,'Queued for Processing'), (2,'Processing by Warehouse'), (3,'Queued for Dispatch'), (4,'Dispatched'), (5,'Delivered')), default=1)
    priority = models.IntegerField(choices=((1,'Low'),(2,'Medium'),(3,'High')), default=2)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    time_placed = models.DateTimeField(auto_now_add=True, blank=True)
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()

