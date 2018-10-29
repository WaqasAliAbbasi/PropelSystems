from django.shortcuts import render
from django.http import HttpResponse

from home.models import Order

# Create your views here.

distancedict={
    'Mui Wo Clinic': [('North Lamma Clinic',12.54), 
    ('Peng Chau Clinic',4.68),
    ('Sok Kwu Wan Clinic', 15.32), 
    ('Tai O Clinic', 14.44), 
    ('Aberdeen Clinic', 16.41), 
    ('Ap Lei Chau Clinic', 16.24), 
    ('Queen Mary Hospital', 13.74)],
    'North Lamma Clinic':[('Peng Chau Clinic', 9.92),
    ('Sok Kwu Wan Clinic',2.96),
    ('Tai O Clinic', 26.29),
    ('Aberdeen Clinic', 5.45),
    ('Ap Lei Chau Clinic', 4.87),
    ('Queen Mary Hospital', 5.52)],
    'Peng Chau Clinic':[('Sok Kwu Wan Clinic', 12.88),
    ('Tai O Clinic', 18.90),
    ('Aberdeen Clinic', 12.64),
    ('Ap Lei Chau Clinic', 12.62),
    ('Queen Mary Hospital', 9.61)],
    'Sok Kwu Wan Clinic':[('Tai O Clinic', 28.71),
    ('Aberdeen Clinic', 5.53),
    ('Ap Lei Chau Clinic', 4.77),
    ('Queen Mary Hospital', 7.19)],
    'Tai O Clinic':[('Aberdeen Clinic',30.72),
    ('Ap Lei Chau Clinic',30.47),
    ('Queen Mary Hospital',28.18)],
    'Aberdeen Clinic':[('Ap Lei Chau Clinic',0.77),
    ('Queen Mary Hospital',3.44)],
    'Ap Lei Chau Clinic':[('Queen Mary Hospital',3.79)]
}

def index(request):
    orders = Order.objects.all()
    context = {
        'items': orders
    }
    return render(request, 'dispatch/index.html', context)
