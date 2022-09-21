from django.contrib import admin
from user.models import User
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin


# admin.site.register(User)


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model"""

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "is_employee",
                    "is_restaurant_staff",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
    )
    list_display = (
        "username",
        "first_name",
        "last_name",
        "is_employee",
        "is_restaurant_staff",
    )
    search_fields = ("username", "first_name", "last_name")
    ordering = ("username",)
