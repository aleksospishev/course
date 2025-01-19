# Register your models here.
from django.contrib import admin

from .models import User


@admin.register(User)
class Useradmin(admin.ModelAdmin):
    """Модель администрирования пользователей."""

    list_display = (
        "email",
        "avatar",
    )
    list_filter = ("email",)
    search_fields = ("email",)
