from django.urls import path

from . import views

app_name = 'warehouse'
urlpatterns = [
    path('', views.warehouse, name='warehouse'),
    path('process_next_order', views.process_next_order, name='process_next_order'),
    path('view_order_details', views.view_order_details, name='view_order_details'),
    path('get_order_label', views.get_order_label, name='get_order_label'),
    path('move_to_dispatch', views.move_to_dispatch, name='move_to_dispatch')
]
