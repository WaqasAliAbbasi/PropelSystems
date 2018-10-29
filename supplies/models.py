from django.db import models
from home.models import Warehouse

class Category(models.Model):
    name = models.CharField(max_length=200)

class Item(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    shipping_weight_grams = models.PositiveIntegerField()
