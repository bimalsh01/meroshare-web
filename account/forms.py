from django.core import validators
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms
from django.forms import ModelForm
from account.models import Meroshare

class UserForm(UserCreationForm):
    """Form for creating Users"""
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['first_name', 'last_name','email','username','password1','password2']


class LoginForm(forms.Form):
    """Form to allow users to log in"""
    username = forms.CharField(validators=[validators.MinLengthValidator(3)])
    password = forms.CharField(widget=forms.PasswordInput)

class MeroshareForm(ModelForm):
    class Meta:
        model = Meroshare
        fields = ['name','dp','uname','pword','crn','pin']