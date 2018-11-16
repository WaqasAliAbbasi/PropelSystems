from django.shortcuts import render
from django.http import HttpResponse
from .models import User

access = {
    User.ADMIN: [
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
}

def index(request):
    links = ''
    for role in access:
        for link in access[role]:
            links += "<li><a href='" + link[1] + "'>" + link[0] + "</a></li>"

    return HttpResponse(
        "<h1>AS-P Homepage</h1><ul>" + links + "</ul>"
    )
