from django.urls import path

from users.views import login_view, logout_view, profile_edit, register, home, profile


urlpatterns = [
    path("", home, name="home"),
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile-edit/", profile_edit, name="profile_edit"),
    path("profile/", profile, name="profile"),

]
