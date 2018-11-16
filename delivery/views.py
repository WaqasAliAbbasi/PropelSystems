from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from home.decorators import clinic_manager_required
from home.views import access
from home.models import Order

@login_required
@clinic_manager_required
def delivery(request):
    orders = Order.objects.filter(clinic=request.user.clinic, status=Order.DISPATCHED).order_by('time_dispatched')
    context = {
        'sidebar': access[request.user.role],
        'name': request.user.get_full_name(),
        'location': request.user.clinic.name,
        'role': request.user.get_role_display,
        'orders': orders
    }
    return render(request, 'delivery/index.html', context)
