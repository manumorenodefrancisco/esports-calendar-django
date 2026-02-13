from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from Users.models import User


class CustomUserAdmin(UserAdmin):
    list_display = ("email", "username", "role__name", "is_active", 'is_staff', "is_superuser")
    list_filter = ("is_active", 'is_superuser')
    search_fields = ("email", "first_name")
    ordering = ("-email", 'is_superuser')
    readonly_fields = ("username",)

    fieldsets = (
        ("Inicio de sesión", {
            "classes": ("wide",),
            "fields": ("email", "password", "role"),
        }),
        ("Información personal", {
            "classes": ("wide",),
            "fields": ("username", "first_name", "last_name", "is_active", "is_staff", "is_superuser"),
        })
    )

    add_fieldsets = (
        ("Inicio de sesión", {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "role"),
        }),
        ("Información personal", {
            "classes": ("wide",),
            "fields": ("username", "first_name", "last_name", "is_active", "is_staff", "is_superuser"),
        })
    )


admin.site.register(User, CustomUserAdmin)
