from django.urls import path

from . import views

app_name = 'supplies'
urlpatterns = [
    path('', views.supplies, name='supplies'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('flush_session', views.flush_session, name='flush_session'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
]
