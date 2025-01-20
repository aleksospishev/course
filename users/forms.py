from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from users.models import User


class UserRegisterForm(UserCreationForm):
    """Форма регистрации нового пользователя."""

    class Meta:
        model = User
        fields = ["email", "password1", "password2", "avatar"]

class UserUpdateForm(ModelForm):

    class Meta:
        model = User
        fields = ["avatar"]



