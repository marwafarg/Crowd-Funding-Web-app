from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms


class signup(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address')
    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password1','password2','mobile_phone','profile_photo']