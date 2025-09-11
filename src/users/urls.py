from django.urls import path

from users.views import login_view, logout_view, register, home


urlpatterns = [
    path("", home, name="home"),
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout")

]
