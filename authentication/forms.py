from django import forms
from django.contrib.auth.forms import UserCreationForm
from home.models import User

class InviteForm(forms.Form):
    email = forms.EmailField(max_length=200, help_text='Required')
    role = forms.IntegerField(required=True, help_text='Required')

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name')
