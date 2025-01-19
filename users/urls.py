from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import (
    NewPasswordResetCompleteView,
    NewPasswordResetConfirmView,
    NewPasswordResetDoneView,
    NewPasswordResetView,
    UserRegisterView,
    verification_email,
    UserDetailView,
    UserUpdateView,
    UserDeleteView
)

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("email-confirm/<str:token>/", verification_email, name="email-confirm"),
    path("password-reset/", NewPasswordResetView.as_view(), name="password_reset"),
    path(
        "password-reset/done/",
        NewPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "password-reset/confirm/<str:uidb64>/<str:token>/",
        NewPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/complete/",
        NewPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("update/<int:pk>", UserUpdateView.as_view(), name="user-update"),
    path("delete/<int:pk>",UserDeleteView.as_view(), name="user-delete"),

]
