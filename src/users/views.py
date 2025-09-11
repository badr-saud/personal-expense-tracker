from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from users.forms import UserCreationFrom, UserLoginForm


# Create your views here.
@login_required(login_url="login")
def home(request):
    return render(request, "users/home.html")

def register(request):
    if request.method == "POST":
        form = UserCreationFrom(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            return redirect("login")
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
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password")

    form = UserLoginForm()
    return render(request, "users/login.html", {"form": form})

def logout_view(request):
    logout(request)  
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")
