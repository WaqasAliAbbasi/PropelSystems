from django.urls import path

from . import views

app_name = 'dispatch'
urlpatterns = [
    path('', views.dispatch, name='dispatch'),
    path('dispatch_shipment', views.dispatch_shipment, name='dispatch_shipment'),
    path('get_itinerary', views.get_itinerary, name='get_itinerary')
]
