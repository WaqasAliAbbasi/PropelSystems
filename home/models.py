from django.db import models
from django.contrib.auth.models import AbstractUser

class Location(models.Model):
    name = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    altitude_meters = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class User(AbstractUser):
    ADMIN = 0
    CLINIC_MANAGER = 1
    WAREHOUSE_PERSONNEL = 2
    DISPATCHER = 3
    HOSPITAL_AUTHORITY = 4

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (CLINIC_MANAGER, 'Clinic Manager'),
        (WAREHOUSE_PERSONNEL, 'Warehouse Personnel'),
        (DISPATCHER, 'Dispatcher'),
        (HOSPITAL_AUTHORITY, 'Hospital Authority'),
    )

    username = models.CharField(max_length=10,default= None, null=True)
    email = models.EmailField(unique=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank = True, null = True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Distance(models.Model):
    location_from = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='location_from')
    location_to = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='location_to')
    distance = models.DecimalField(max_digits=9, decimal_places=2)

class Warehouse(Location):
    pass

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Item(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='item_images')
    shipping_weight_grams = models.PositiveIntegerField()

    def __str__(self):
        return self.description

class Clinic(Location):
    linked_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)

class Order(models.Model):
    QUEUED_FOR_PROCESSING = 1
    PROCESSING_BY_WAREHOUSE = 2
    QUEUED_FOR_DISPATCH = 3
    DISPATCHED = 4
    DELIVERED = 5
    status = models.IntegerField(choices=((QUEUED_FOR_PROCESSING ,'Queued for Processing'), (PROCESSING_BY_WAREHOUSE,'Processing by Warehouse'), (QUEUED_FOR_DISPATCH,'Queued for Dispatch'), (DISPATCHED,'Dispatched'), (DELIVERED,'Delivered')), default=1)

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    priority = models.IntegerField(choices=((LOW,'Low'),(MEDIUM,'Medium'),(HIGH,'High')), default=2)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    time_placed = models.DateTimeField(auto_now_add=True)
    time_dispatched = models.DateTimeField(blank=True, editable=False, null=True)

    def __str__(self):
        return 'Order #' + str(self.id) + ' - ' + self.clinic.name + ' - ' + self.time_placed.strftime("%c")


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def orderitem_details(self):
        return str(self.quantity) + ' x ' + str(self.item)

    def __str__(self):
        return 'Order #' + str(self.order.id) + ' - ' + str(self.quantity) + ' x ' + str(self.item)
