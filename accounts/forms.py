from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label="Электронная почта",
    )

    full_name = forms.CharField(
        label="Полное имя",
        max_length=255,
    )

    class Meta:
        model = User

        fields = (
            "username",
            "email",
            "full_name",
        )

        labels = {
            "username": "Логин",
        }


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Логин",
        max_length=150,
    )

    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
    )