from django.contrib.auth.models import User
from django.db import models

from .utils import (get_country_choices, get_currency_choices,
                    get_timezone_choices)

# Create your models here.

choices = get_currency_choices()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    country = models.CharField(choices=get_country_choices())
    currency = models.CharField(max_length=100, choices=choices)
    timezone = models.CharField(choices=get_timezone_choices())


    def __str__(self):
        return f"{self.user.username}'s profile"
