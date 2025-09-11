from django.db import models
from django.contrib.auth.models import User
from .utils import get_currency_choices

# Create your models here.

choices = get_currency_choices()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    currency = models.CharField(max_length=100, choices=choices)

    def __str__(self):
        return f"{self.user.username}'s profile"
