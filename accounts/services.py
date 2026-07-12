from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from django.db import transaction

from .models import User


@transaction.atomic
def register_user(
    *,
    username: str,
    email: str,
    full_name: str,
    password: str,
) -> User:
    """
    Создаёт нового пользователя.

    Все зарегистрированные через сайт пользователи
    получают роль STUDENT.
    """

    return User.objects.create_user(
        username=username,
        email=email,
        full_name=full_name,
        password=password,
        role=User.Role.STUDENT,
    )


def authenticate_user(
    *,
    request,
    username: str,
    password: str,
):
    """
    Проверяет логин и пароль.

    Возвращает пользователя при правильных данных
    или None при неправильных.
    """

    return authenticate(
        request=request,
        username=username,
        password=password,
    )


def login_user(*, request, user: User) -> None:
    """
    Авторизует пользователя.
    """

    login(request, user)


def logout_user(*, request) -> None:
    """
    Завершает пользовательскую сессию.
    """

    logout(request)


def can_manage_disciplines(user) -> bool:
    """
    Проверяет право пользователя
    создавать и изменять дисциплины.
    """

    if not user.is_authenticated:
        return False

    return (
        user.is_superuser
        or user.role == User.Role.TEACHER
        or user.role == User.Role.ADMIN
    )


def ensure_can_manage_disciplines(user) -> None:
    """
    Вызывает ошибку 403,
    если пользователь не имеет нужной роли.
    """

    if not can_manage_disciplines(user):
        raise PermissionDenied(
            "У вас нет прав для управления дисциплинами."
        )