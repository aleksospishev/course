from django.urls import path, include

from mail.views import (
    HomeView,
    RecipientCreateView,
    RecipientView,
    RecipientDetailView,
    RecipientUpdateView,
    RecipientDeleteView,
    MessageCreateView,
    MessageDeleteView,
    MessageUpdateView,
    MessageDetailView,
    MessageView,
    SendingView,
    SendingCreateView,
    SendingDeleteView,
    SendingDetailView,
    SendingUpdateView,
    SendMessage,
SendMessageCancel
)
from mail.apps import MailConfig

app_name = MailConfig.name

urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path("recipients/", RecipientView.as_view(), name="recipients"),
    path("recipient/<int:pk>/", RecipientDetailView.as_view(), name="recipient"),
    path("recipients/create/", RecipientCreateView.as_view(), name="recipient-create"),
    path(
        "recipients/update/<int:pk>/",
        RecipientUpdateView.as_view(),
        name="recipient-update",
    ),
    path(
        "recipient/delete/<int:pk>/",
        RecipientDeleteView.as_view(),
        name="recipient-delete",
    ),
    path("messages/", MessageView.as_view(), name="messages"),
    path("message/<int:pk>/", MessageDetailView.as_view(), name="message"),
    path("message/create/", MessageCreateView.as_view(), name="message-create"),
    path(
        "message/update/<int:pk>/", MessageUpdateView.as_view(), name="message-update"
    ),
    path(
        "message/delete/<int:pk>/", MessageDeleteView.as_view(), name="message-delete"
    ),
    path("sendings/", SendingView.as_view(), name="sendings"),
    path("sending/<int:pk>/", SendingDetailView.as_view(), name="sending"),
    path("sending/create/", SendingCreateView.as_view(), name="sending-create"),
    path(
        "sending/update/<int:pk>/", SendingUpdateView.as_view(), name="sending-update"
    ),
    path(
        "sending/delete/<int:pk>/", SendingDeleteView.as_view(), name="sending-delete"
    ),
    path("sending/send/<int:pk>/", SendMessage.as_view(), name="send-message"),
    path("sending/cancel/<int:pk>/", SendMessageCancel.as_view(), name="send-message-cancel"),
]
