from django.urls import path

from . import views

app_name = 'supplies'
urlpatterns = [
    path('', views.index, name='index'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('flush_session', views.flush_session, name='flush_session'),
]
