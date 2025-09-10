from django.urls import path

from users.views import login, logout, register, test


urlpatterns = [
    path("", test),
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout")

]
