from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required

from .forms import InviteForm, SignupFormClinic, SignupFormNonClinic
from .tokens import account_activation_token

from home.models import User, Warehouse
from home.views import access

from home.decorators import admin_required
import json

def home(request):
    return render(request, 'home.html')

@login_required
@admin_required
def invite(request):
    if request.method == 'POST':
        form = InviteForm(request.POST)
        if form.is_valid():
            user = User(
                email=form.cleaned_data.get('email'),
                role=int(form.cleaned_data.get('role')),
                is_active=False
            )
            if user.role == User.ADMIN:
                user.is_staff = True
                user.is_superuser = True
            if user.role == User.WAREHOUSE_PERSONNEL or user.role == User.DISPATCHER:
                user.warehouse = Warehouse.objects.all().first()
            user.save()

            email = EmailMessage(
                'Sign Up for your AS-P Account',
                render_to_string('send_email.html', {
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token': account_activation_token.make_token(user),
                }),
                to=[form.cleaned_data.get('email')]
            )
            email.send()
            context = {
                'sidebar': access[request.user.role],
                'message': "Registration invite has been sent to " + user.email + "."
            }
            return render(request, 'message.html', context)
    else:
        form = InviteForm()
    return render(request, 'signup.html', {'title': 'Invite Users', 'form': form, 'sidebar': access[request.user.role]})

def signup(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        context = {
            'message': "Activation link is invalid!"
        }
        return render(request, 'message.html', context)

    if user.role == User.CLINIC_MANAGER:
        SignupFormClass = SignupFormClinic
    else:
        SignupFormClass = SignupFormNonClinic
    if request.method == 'POST':
        form = SignupFormClass(request.POST)
        if form.is_valid():
            if account_activation_token.check_token(user, token):
                user.username = form.cleaned_data.get('username')
                user.first_name = form.cleaned_data.get('first_name')
                user.last_name = form.cleaned_data.get('last_name')
                user.clinic = form.cleaned_data.get('clinic')
                user.set_password(form.cleaned_data.get('password1'))

                user.is_active = True
                user.save()

                login(request, user)
                return redirect(access[user.role][0][1])
            else:
                context = {
                    'message': "Activation link is invalid!"
                }
                return render(request, 'message.html', context)
    else:
        form = SignupFormClass()
    return render(request, 'signup.html', {'title': 'Sign Up', 'form': form})
