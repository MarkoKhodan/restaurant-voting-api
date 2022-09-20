import datetime
import os


from django.db import models
from django.utils.text import slugify

from user.models import User


def menu_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = (
        f"{slugify(instance.restaurant.name)}-{datetime.datetime.now()}{extension}"
    )

    return os.path.join("uploads/menus/", filename)


class Restaurant(models.Model):
    responsible_for_updating = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="restaurant"
    )
    name = models.CharField(max_length=64, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"


class Menu(models.Model):
    file = models.FileField(null=True, upload_to=menu_file_path)
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="menus"
    )
    created_at = models.DateTimeField(auto_now=True)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.restaurant.name} {self.created_at}"


class Employee(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name}, {self.user.last_name}"


class Vote(models.Model):

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee}"
