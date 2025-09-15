from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from users.forms import (UserCreationFrom, UserForm, UserLoginForm,
                         UserProfileForm)


# Create your views here.
@login_required(login_url="login")
def home(request):
    return render(request, "users/home.html")


@login_required(login_url="login")
def profile(request):
    return render(request, "users/profile.html")


@login_required(login_url="login")
def profile_edit(request):
    user = request.user
    profile = user.profile
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
