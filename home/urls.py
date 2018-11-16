from django.urls import path
from .models import User
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.index, name='index'),
]
