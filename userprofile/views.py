from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from .forms import EditProfileForm

def profilepage(request):
    return render(request, 'profile.html')  

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/userprofile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'changepassword.html', {
        'form': form
    })

def edit_profile(request):
    user = request.user
    form = EditProfileForm(request.POST or None, initial={'first_name':user.first_name, 'last_name':user.last_name, 'email':user.email})
    if request.method == 'POST':
        if form.is_valid():


            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.save()
            return redirect('/userprofile')

    context = {
        "form": form
    }

    return render(request, "edit_profile.html", context)

