from django import forms
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    profile_pic = forms.ImageField(required=False)

