from django.shortcuts import render
from django.http import HttpResponse
from .models import User

access = {
    User.ADMIN: [
        ["Admin","/admin"],
        ["Invite","/auth/invite"],
        ["Profile", "/userprofile"]
    ],
    User.CLINIC_MANAGER: [
        ["Supplies","/supplies"],
        ["Orders","/orders"],
        ["Profile", "/userprofile"]
    ],
    User.WAREHOUSE_PERSONNEL: [
        ["Warehouse","/warehouse"],
        ["Profile", "/userprofile"]
    ],
    User.DISPATCHER: [
        ["Dispatch","/dispatch"],
        ["Profile", "/userprofile"]
    ],
    User.HOSPITAL_AUTHORITY: [
        ["Admin","/admin"],
        ["Profile", "/userprofile"]
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
