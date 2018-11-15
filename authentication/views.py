from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import InviteForm, SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from home.models import User
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
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
                role=form.cleaned_data.get('role'),
                is_active=False
            )
            if user.role == User.ADMIN:
                user.is_staff = True
                user.is_superuser = True
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

            return HttpResponse('An invitation email has been sent to the user.')
    else:
        form = InviteForm()
    return render(request, 'signup.html', {'title': 'Invite Users', 'form': form})

def signup(request, uidb64, token):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            try:
                uid = urlsafe_base64_decode(uidb64).decode()
                user = User.objects.get(pk=uid)
            except(TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None

            if user is not None and account_activation_token.check_token(user, token):
                user.username = form.cleaned_data.get('username')
                user.first_name = form.cleaned_data.get('first_name')
                user.last_name = form.cleaned_data.get('last_name')
                user.set_password(form.cleaned_data.get('password1'))

                user.is_active = True
                user.save()

                login(request, user)
                return redirect('/')
            else:
                return HttpResponse('Activation link is invalid!')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'title': 'Sign Up', 'form': form})
