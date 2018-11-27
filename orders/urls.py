from django.urls import path

from . import views

app_name = 'orders'
urlpatterns = [
    path('', views.orders, name='orders'),
    path('cancel', views.cancel, name='cancel'),
    path('notify_delivery', views.notify_delivery, name='notify_delivery')
]
