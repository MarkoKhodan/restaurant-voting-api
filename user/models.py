from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_employee = models.BooleanField(default=False)
    is_restaurant_staff = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username}"
