from django.db import models
from django.db.models import CASCADE
from users.models import User




class Recipient(models.Model):
    """Получатель рассылки."""

    email = models.EmailField(unique=True, verbose_name="email")
    name = models.CharField(max_length=100, verbose_name="ФИО")
    comment = models.TextField(max_length=500, verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, related_name="owner_recipient", on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.email}"

    class Meta:
        verbose_name = "Получатель рассылки"
        verbose_name_plural = "Получатели рассылки"
        ordering = ["-created_at"]
        permissions = [("can_view_all_recipints_lists", "can view all recipients lists")]



class Message(models.Model):
    """Сообщение с темой и телом письма."""

    subject = models.CharField(max_length=200, verbose_name="Тема письма")
    content = models.TextField(verbose_name="Тело письма")
    owner = models.ForeignKey(User, related_name="owner_message", on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["subject"]
        permissions = [("can_view_all_message_lists", "can view all message lists")]



class Sending(models.Model):
    """Рассылка сообщений."""

    first_sending = models.DateTimeField(verbose_name="Дата первой рассылки")
    stop_sending = models.DateTimeField(verbose_name="Дата первой рассылки")
    status = models.CharField(verbose_name="Статус рассылки", default="Создана")
    message = models.ForeignKey(
        Message, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Письмо"
    )
    recipients = models.ManyToManyField(
        Recipient,
        related_name="recipients",
    )
    owner = models.ForeignKey(User, related_name="owner_sending", on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"Рассылка {id}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["-first_sending"]
        permissions = [("can_disable_mailing", "can disable mailing"),
            ("can_view_all_sendings_list", "can view all sendings list")]


class AtemptSending(models.Model):
    date_atempt = models.DateTimeField(auto_now_add=True)
    status = models.CharField(verbose_name="статус рассылки")
    server_response = models.TextField(verbose_name="Ответ почтового сервера")
    sending = models.ForeignKey(
        Sending, on_delete=models.CASCADE, related_name="sending"
    )

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"
        ordering = ["-date_atempt"]
