
from django.core.cache import cache

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
    DetailView,
)
from smtplib import SMTPException
from mail.forms import RecipientForm, MessageForm, SendingForm
from mail.models import Recipient, Message, Sending, AtemptSending
from django.core.mail import send_mail
from course_django.settings import EMAIL_HOST_USER


class HomeView(TemplateView):
    template_name = "mail/home.html"
    extra_context = {"title": "Домашняя страница"}
    context_object_name = "context_home"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sendings_total"] = len(Sending.objects.all())
        context["sendings_active_count"] = len(Sending.objects.filter(status="Запущена"))
        context["recipients_total"] = len(Recipient.objects.all())
        context['sendings'] = Sending.objects.filter(status='Запущена')
        return context


class RecipientView(LoginRequiredMixin, ListView):
    """Список всех получателей рассылок."""

    model = Recipient
    extra_context = {"title": "Список получателей"}


    def get_queryset(self):
        queryset = cache.get("recipients_list")
        if not queryset:
            if self.request.user.has_perm("recipient.can_view_all_recipient_lists") or self.request.user.groups.filter(name="Менеджеры"):
                queryset = Recipient.objects.all()
                cache.set("recipient_list", queryset, 60)
            else:
                queryset = Recipient.objects.filter(owner=self.request.user)
                cache.set("recipient_list", queryset, 60)
        return queryset



class RecipientDetailView(LoginRequiredMixin, DetailView):
    """Детальный просмотр получателя рассылки."""

    model = Recipient
    form_class = RecipientForm


    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.groups.filter(name="Менеджеры") or self.request.user.is_superuser :
            return self.object
        if self.object.owner != self.request.user and not self.request.user.is_superuser :
            raise PermissionDenied
        return self.object



class RecipientCreateView(LoginRequiredMixin, CreateView):
    """Создание нового получателя рассылки."""

    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("mail:recipients")

    def form_valid(self, form):
        recipient = form.save()
        recipient.owner = self.request.user
        recipient.save()
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    """Изменение информации о получателе рассылки."""

    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("mail:recipients")

    def form_valid(self, form):
        recipient = form.save()
        recipient.owner = self.request.user
        recipient.save()
        return super().form_valid(form)

    def get_queryset(self):
        user = self.request.user
        obj = get_object_or_404(Recipient, id=self.kwargs['pk'])
        if obj:
            if self.request.user.has_perm('recipient.can_view_all_recipints_lists') or user == obj.owner or self.request.user.groups.filter(name='Менеджеры'):
                return Recipient.objects.all()
            else:
                raise PermissionDenied


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление получателя рассылки."""

    model = Recipient

    def get_success_url(self):
        return reverse_lazy("mail:recipients")

    def has_permission(self):
        obj = self.get_object()
        return obj.owner == self.request.user


class MessageView(LoginRequiredMixin, ListView):
    """Список всех рассылок сообщений."""

    model = Message

    def get_queryset(self):
        queryset = cache.get("message_list")
        if not queryset:
            if self.request.user.has_perm("message.can_view_all_message_lists") or self.request.user.groups.filter(name='Менеджеры') :
                queryset = Message.objects.all()
                cache.set("message_list", queryset, 60)
            else:
                queryset = Message.objects.filter(owner=self.request.user)
                cache.set("message_list", queryset, 60)
        return queryset


class MessageDetailView(LoginRequiredMixin, DetailView):
    """Детальный просмотр сообщений."""

    model = Message
    form_class = MessageForm


    def get_queryset(self):
        if self.request.user.has_perm('can_view_all_recipints_lists'):
            return Recipient.objects.all()
        return Recipient.objects.filter(owner=self.request.user)

class MessageCreateView(LoginRequiredMixin, CreateView):
    """Создание нового сообщения."""

    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mail:messages")

    def form_valid(self, form):
        message = form.save()
        message.owner = self.request.user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """Изменение информации о получателе рассылки."""

    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mail:messages")

    def form_valid(self, form):
        message = form.save()
        message.owner = self.request.user
        message.save()
        return super().form_valid(form)



class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление получателя рассылки."""

    model = Message

    def get_success_url(self):
        return reverse_lazy("mail:messages")


class SendingView(LoginRequiredMixin, ListView):
    """Список всех рассылок сообщений."""

    model = Sending

    def get_queryset(self):
        queryset = cache.get("sending_list")
        if not queryset:
            if self.request.user.has_perm("sending.can_view_all_sending_lists"):
                queryset = Sending.objects.all()
                cache.set("sending_list", queryset, 60)
            else:
                queryset = Sending.objects.filter(owner=self.request.user)
                cache.set("sending_list", queryset, 60)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['all_sendings'] = Sending.objects.all()
        return context


class SendingDetailView(LoginRequiredMixin, DetailView):
    """Детальный просмотр сообщений."""

    model = Sending
    form_class = SendingForm


class SendingCreateView(LoginRequiredMixin, CreateView):
    """Создание нового сообщения."""

    model = Sending
    form_class = SendingForm
    success_url = reverse_lazy("mail:sendings")

    def form_valid(self, form):
        sending = form.save()
        sending.owner = self.request.user
        sending.save()
        return super().form_valid(form)


class SendingUpdateView(LoginRequiredMixin, UpdateView):
    """Изменение информации о получателе рассылки."""

    model = Sending
    form_class = SendingForm
    success_url = reverse_lazy("mail:sending")

    def form_valid(self, form):
        sending = form.save()
        sending.owner = self.request.user
        sending.save()
        return super().form_valid(form)


class SendingDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление получателя рассылки."""

    model = Sending

    def get_success_url(self):
        return reverse_lazy("mail:sendings")


class SendMessage(View):
    def post(self, request, pk):
        sending = get_object_or_404(Sending, pk=pk)
        user = self.request.user

        try:
            send_mail(
                subject=sending.message.subject,
                message=sending.message.content,
                from_email=EMAIL_HOST_USER,
                recipient_list=[recipient.email for recipient in sending.recipients.all()],
            )
            sending.status = "Запущена"
            sending.save()
        except SMTPException as error:
            atempt_send = AtemptSending(status='Не успешно', server_response=error, sending=sending)
            atempt_send.save()
            user.amount_failed += 1
            user.save()
        else:
            atempt_send = AtemptSending(status='Успешно', server_response='письмо отправлено', sending=sending)
            atempt_send.save()
            user.amount_attempt += 1
            user.save()
            return redirect("mail:home")


class SendMessageCancel(View):
    def post(self, request, pk):
        sending = get_object_or_404(Sending, pk=pk)
        sending.status = "Завершена"
        sending.save()
        return redirect("mail:home")