from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 
from django.http import JsonResponse
from django.views.decorators.http import require_GET 
from django.shortcuts import redirect, render

from users.forms import (UserCreationFrom, UserForm, UserLoginForm,
                         UserProfileForm)
from users.models import UserProfile
from users.utils import get_timezones_for_country


# Create your views here.
@require_GET
def get_timezone_for_country_view(request):
    """endpoint to get the timezones for a specific country (for profile edit and JS)"""
    country = request.GET.get("country")
    if not country:
        return JsonResponse({"error": "country code required"}, status=400)

    choices = get_timezones_for_country(country)
    timezones = [{"value": tz[0], "label": tz[1]} for tz in choices]
    return JsonResponse({"timezones": timezones})


@login_required(login_url="login")
def home(request):
    return render(request, "users/home.html")


@login_required(login_url="login")
def profile(request):
    return render(request, "users/profile.html")


@login_required(login_url="login")
def profile_edit(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    if request.method == "POST":
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserForm(request.POST, request.FILES, instance=user)

        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            return redirect("profile")
    else:
        profile_form = UserProfileForm(instance=profile)
        user_form = UserForm(instance=user)
        return render(
            request,
            "users/edit_profile.html",
            {"user_form": user_form, "profile_form": profile_form},
        )


def register(request):
    if request.method == "POST":
        form = UserCreationFrom(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            return redirect("profile")
    else:
        form = UserCreationFrom()
    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back: {user.username}!")
                next_url = request.GET.get("next") or request.POST.get("next")
                return redirect(next_url or "home")

            else:
                messages.error(request, "Invalid username or password")

    form = UserLoginForm()
    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")
