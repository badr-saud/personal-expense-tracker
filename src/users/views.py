from django.shortcuts import render

from users.forms import UserCreationFrom


# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserCreationFrom(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            return render(request, "home.html")
    else:
        form = UserCreationFrom()
    return render(request, "users/register.html", {"form": form})

def test(request):
    return render(request, "base.html")

def login(request):
    pass

def logout(request):
    pass

