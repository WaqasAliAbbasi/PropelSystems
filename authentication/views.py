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
import json

def home(request):
    return render(request, 'home.html')

def invite(request):
    if request.method == 'POST':
        form = InviteForm(request.POST)
        if form.is_valid():
            user = User(
                email=form.cleaned_data.get('email'),
                role=form.cleaned_data.get('role'),
                is_active=False
            )
            user.save() 
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('send_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
    else:
        form = InviteForm()
    return render(request, 'signup.html', {'form': form})

def activate_user(request, uidb64, token):
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
                # return redirect('home')
                return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
            else:
                return HttpResponse('Activation link is invalid!')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def invite_user_page(request): 
    return render(request, 'invite_user.html')

def send_invite_email(request):  
    if request.method == 'POST':
        emailID = request.POST.get('email')
        link = 'http://localhost:8000/authentication/signup/?email='+emailID
        message = 'Click the following link to register for AS-P ' + link
        mail_subject = 'Invitation for AS-P'
        email = EmailMessage(
                mail_subject, message, to=[emailID]
            )
        email.send()
        return HttpResponse('Email Sent')