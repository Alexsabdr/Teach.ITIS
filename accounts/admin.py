from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Project fields", {"fields": ("full_name", "role")}),
    ) # type: ignore
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Project fields", {"fields": ("email", "full_name", "role")}),
    )
    list_display = ("username", "email", "full_name", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "email", "full_name")
