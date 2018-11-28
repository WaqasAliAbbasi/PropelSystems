from django import forms
from home.models import User

class EditProfileForm(forms.Form):

    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    email = forms.CharField(label='email')  

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']