from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('invite/', views.invite, name='invite'),
    path('signup/<uidb64>/<token>', views.signup, name='signup'),
]
