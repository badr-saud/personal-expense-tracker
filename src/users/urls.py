from django.urls import path

from users.views import get_timezone_for_country_view, login_view, logout_view, profile_edit, register, home, profile


urlpatterns = [
    path("", home, name="home"),
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile-edit/", profile_edit, name="profile_edit"),
    path("profile/", profile, name="profile"),
    # url for getting a list of timezones for a specific country 
    path("ajax/get-timezones/", get_timezone_for_country_view, name="get_timezones"),

]
