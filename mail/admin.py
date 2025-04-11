from django.contrib import admin

from .models import Recipient, Message, Sending, AtemptSending


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "comment", "created_at", "updated_at", "owner")
    search_fields = ("email", "name", "comment")
    list_filter = ("email", "created_at")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "content", "owner")
    search_fields = ("subject", "content")
    list_filter = ("subject",)


@admin.register(Sending)
class SendingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_sending",
        "stop_sending",
        "status",
        "owner"
    )
    search_fields = (
        "id",
        "first_sending",
        "stop_sending",
        "status",
    )
    list_filter = ("first_sending", "status")


@admin.register(AtemptSending)
class AtemptSendingAdmin(admin.ModelAdmin):
    list_display = ("id", "date_atempt", "status", "server_response",)
    search_fields = ("id", "status", "server_response")
    list_filter = ("date_atempt", "status", "server_response")
