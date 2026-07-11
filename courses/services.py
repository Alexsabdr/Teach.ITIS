from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Count, Q

from accounts.models import User

from .models import Discipline


SORT_OPTIONS = {
    "title": "title",
    "newest": "-created_at",
    "oldest": "created_at",
}


def get_filtered_disciplines(
    *,
    search_query: str = "",
    author_id: str = "",
    sort: str = "title",
):
    """
    Возвращает список дисциплин
    с применёнными поиском, фильтрацией и сортировкой.
    """

    disciplines = (
        Discipline.objects
        .select_related("created_by")
        .annotate(
            topics_count=Count("topics")
        )
    )

    if search_query:
        disciplines = disciplines.filter(
            Q(
                title__icontains=search_query
            )
            | Q(
                description__icontains=search_query
            )
            | Q(
                created_by__username__icontains=search_query
            )
            | Q(
                created_by__full_name__icontains=search_query
            )
        )

    if author_id.isdigit():
        disciplines = disciplines.filter(
            created_by_id=int(author_id)
        )

    ordering = SORT_OPTIONS.get(
        sort,
        "title",
    )

    return disciplines.order_by(ordering)


def get_discipline_authors():
    """
    Возвращает пользователей,
    у которых есть созданные дисциплины.
    """

    UserModel = get_user_model()

    return (
        UserModel.objects
        .filter(
            created_disciplines__isnull=False
        )
        .distinct()
        .order_by("username")
    )


@transaction.atomic
def create_discipline(
    *,
    form,
    user,
) -> Discipline:
    """
    Создаёт дисциплину
    и автоматически назначает автора.
    """

    discipline = form.save(
        commit=False
    )

    discipline.created_by = user

    discipline.save()

    return discipline


@transaction.atomic
def update_discipline(
    *,
    form,
) -> Discipline:
    """
    Сохраняет изменения дисциплины.
    """

    return form.save()


def can_edit_discipline(
    *,
    user,
    discipline: Discipline,
) -> bool:
    """
    Администратор может изменять все дисциплины.

    Преподаватель может изменять
    только созданные им дисциплины.
    """

    if not user.is_authenticated:
        return False

    if (
        user.is_superuser
        or user.role == User.Role.ADMIN
    ):
        return True

    return (
        user.role == User.Role.TEACHER
        and discipline.created_by_id
        == user.id
    )


def ensure_can_edit_discipline(
    *,
    user,
    discipline: Discipline,
) -> None:
    """
    Вызывает ошибку 403,
    если пользователь не может
    изменить дисциплину.
    """

    if not can_edit_discipline(
        user=user,
        discipline=discipline,
    ):
        raise PermissionDenied(
            "Вы можете изменять только "
            "собственные дисциплины."
        )