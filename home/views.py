from django.shortcuts import render
from django.http import HttpResponse
from .models import User

access = {
    User.ADMIN: [
        ["Admin","/admin"],
        ["Invite","/auth/invite"]
    ],
    User.CLINIC_MANAGER: [
        ["Supplies","/supplies"],
        ["Delivery","/delivery"]
    ],
    User.WAREHOUSE_PERSONNEL: [
        ["Warehouse","/warehouse"],
    ],
    User.DISPATCHER: [
        ["Dispatch","/dispatch"],
    ],
    User.HOSPITAL_AUTHORITY: [
        ["Admin","/admin"]
    ],
}

def index(request):
    sidebar = []
    for role in access:
        for link in access[role]:
            if link not in sidebar:
                sidebar.append(link)
    context = {
        'sidebar': list(sidebar),
        'fixed': True
    }
    return render(request, 'home/base.html', context)
