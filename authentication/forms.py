from django import forms
from django.contrib.auth.forms import UserCreationForm
from home.models import User, Clinic

class InviteForm(forms.Form):
    email = forms.EmailField(max_length=200, help_text='Required')
    role = forms.ChoiceField(choices = User.ROLE_CHOICES, label="Role", initial='', widget=forms.Select(), required=True)

    def clean_email(self):
        # Get the email
        email = self.cleaned_data.get('email')

        # Check to see if any users already exist with this email as a username.
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return email

        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('This email address is already in use.')

class SignupFormClinic(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    clinic = forms.ModelChoiceField(queryset=Clinic.objects.all())
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'clinic')

class SignupFormNonClinic(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name')
