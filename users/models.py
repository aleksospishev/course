from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    """Переопределение модели User."""

    username = None
    avatar = models.ImageField(
        upload_to="users/avatars/", blank=True, null=True, verbose_name="Аватар"
    )
    email = models.EmailField(verbose_name="Электронная почта", unique=True)
    token = models.CharField(unique=True, blank=True, null=True)
    amount_attempt = models.IntegerField(
        verbose_name="Количество попыток расыли", default=0
    )
    amount_failed = models.IntegerField(
        verbose_name="Количество не успешных попыток", default=0
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
