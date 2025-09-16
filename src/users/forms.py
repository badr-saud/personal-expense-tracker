from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from users.models import UserProfile
from users.utils import (get_country_iso, get_timezone_choices,
                         get_timezones_for_country)


class UserCreationFrom(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                "placeholder": "Enter your password",
            }
        )
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                "placeholder": "Confirm your password",
            }
        )
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "confirm_password"]
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                    "placeholder": "Enter your username",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                    "placeholder": "Enter your email",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password:
            validate_password(password)
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords does not match!")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                "placeholder": "Enter your username",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                "placeholder": "Enter your password",
            }
        )
    )


class UserProfileForm(forms.ModelForm):
    timezone = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            }
        )
    )

    class Meta:
        model = UserProfile
        fields = ["country", "currency", "timezone"]
        widgets = {
            "country": forms.Select(
                attrs={
                    "class": "w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                }
            ),
            "currency": forms.Select(
                attrs={
                    "class": "w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                }
            ),
            # No need to repeat timezone widget here — already defined above
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        country = None
        if self.instance and self.instance.pk:  # from existing instance
            country = self.instance.country
        elif self.data:  # coming from POST/GET
            country = self.data.get("country")
        elif self.initial:  # from initial data
            country = self.initial.get("country")

        # Set timezone choices based on country or default
        if country:
            choices = get_timezones_for_country(country)
        else:
            choices = get_timezone_choices()

        # Ensure choices is a valid list of tuples
        if not choices:
            choices = [("", "---------")]  # fallback to empty option

        self.fields["timezone"].choices = choices

        # Optional: Set initial value if instance exists
        if self.instance and self.instance.pk and self.instance.timezone:
            self.fields["timezone"].initial = self.instance.timezone


class UserForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                "placeholder": "Enter your email",
            }
        ),
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                    "placeholder": "Enter your first name",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                    "placeholder": "Enter your last name",
                }
            ),
        }
