import secrets

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import (
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView

from course_django.settings import EMAIL_HOST_USER

from users.forms import UserRegisterForm, UserUpdateForm
from users.models import User


class UserRegisterView(CreateView):
    """Регистрация нового пользователя."""

    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        """Сохраняет нового пользователя и отправляет письмо с информацией о регистрации."""
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        self.send_welcome_email(user.email, url)
        return super().form_valid(form)

    def send_welcome_email(self, user_email, path):
        """Отправляет письмо с приветствием и информацией о регистрации."""
        subject = "Добро пожаловать в наш сервис"
        message = f"Спасибо, что   в нашем сервисе! Для подтверждения перейдите по ссылке {path}"
        from_email = EMAIL_HOST_USER
        recipient_list = [user_email]
        send_mail(subject, message, from_email, recipient_list)


def verification_email(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class NewPasswordResetView(PasswordResetView):
    success_url = reverse_lazy("users:password_reset_done")
    template_name = "password-reset.html"
    email_template_name = "password_reset_email.html"


class NewPasswordResetDoneView(PasswordResetDoneView):
    success_url = reverse_lazy("users:login")
    template_name = "reset_done_password.html"


class NewPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy("users:password_reset_complete")
    template_name = "password_reset_confirm.html"


class NewPasswordResetCompleteView(PasswordResetCompleteView):
    success_url = reverse_lazy("users:password_reset_complete")
    template_name = "password_reset_complete.html"


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user_detail.html'


    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.is_superuser or self.request.user == self.object:
            return self.object
        raise PermissionDenied


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy("mail:home")


    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.is_superuser or self.request.user == self.object:
            return self.object
        raise PermissionDenied

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User


    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.is_superuser:
            raise PermissionDenied
        if not self.request.user.is_superuser:
            raise PermissionDenied
        return self.object

