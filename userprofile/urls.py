from django.urls import path

from . import views

app_name = 'userprofile'

urlpatterns = [
    path('password/', views.change_password, name='change_password'),
    path('', views.profilepage, name='profilepage'),
    path('editprofile/', views.edit_profile, name='edit_profile')
]  