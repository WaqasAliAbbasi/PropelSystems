from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('invite/', views.invite, name='invite'),
    path('activate/<uidb64>/<token>', views.activate_user, name='activate'),
    path('send_invite/', views.invite_user_page, name='invite_user_page'),
    path('send_invite_email/', views.send_invite_email, name='send_invite_email')
    # url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate_user, ),
]