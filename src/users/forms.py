from django import forms
from django.contrib.auth.models import User


class UserCreationFrom(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter your username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter your email'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Create a password'
            }),
        }
