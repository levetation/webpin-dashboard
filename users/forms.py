from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder': ''}), label='Email')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': ''}), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': ''}), label='Confirm password')

    class Meta:
        model = CustomUser
        fields = ("email", "password1", "password2")


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email",)