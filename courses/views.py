from .services import (
    can_edit_discipline,
    can_edit_topic,
    create_discipline,
    create_topic,
    ensure_can_edit_discipline,
    ensure_can_edit_topic,
    get_discipline_authors,
    get_filtered_disciplines,
    update_discipline,
    update_topic,
)

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.services import (
    ensure_can_manage_disciplines,
)

from .forms import DisciplineForm, TopicForm
from .models import Discipline, Topic

def discipline_list(request):
    search_query = (
        request.GET
        .get("q", "")
        .strip()
    )

    author_id = (
        request.GET
        .get("author", "")
        .strip()
    )

    sort = (
        request.GET
        .get("sort", "title")
        .strip()
    )

    disciplines = (
        get_filtered_disciplines(
            search_query=search_query,
            author_id=author_id,
            sort=sort,
        )
    )

    context = {
        "disciplines":
            disciplines,

        "authors":
            get_discipline_authors(),

        "search_query":
            search_query,

        "selected_author":
            author_id,

        "selected_sort":
            sort,

        "result_count":
            disciplines.count(),
    }

    return render(
        request,
        "courses/discipline_list.html",
        context,
    )


def discipline_detail(request, slug):
    discipline = get_object_or_404(
        Discipline.objects
        .select_related("created_by")
        .prefetch_related("topics"),
        slug=slug,
    )

    context = {
        "discipline": discipline,
        "can_edit": can_edit_discipline(
            user=request.user,
            discipline=discipline,
        ),
    }

    return render(
        request,
        "courses/discipline_detail.html",
        context,
    )
@login_required
def discipline_create(request):
    ensure_can_manage_disciplines(
        request.user
    )
    if request.method == "POST":
        form = DisciplineForm(request.POST)

        if form.is_valid():
            discipline = create_discipline(
                form=form,
                user=request.user,
            )

            messages.success(
                request,
                "Дисциплина успешно создана.",
            )

            return redirect(
                "courses:discipline_detail",
                slug=discipline.slug,
            )

        else:
            messages.error(
                request,
                "Не удалось создать дисциплину. "
                "Проверьте введённые данные.",
        )

    else:
        form = DisciplineForm()

    context = {
        "form": form,
        "page_title": "Создание дисциплины",
        "button_text": "Создать",
    }

    return render(
        request,
        "courses/discipline_form.html",
        context,
    )

@login_required
def discipline_edit(request, slug):
    ensure_can_manage_disciplines(
        request.user
    )
    discipline = get_object_or_404(
        Discipline,
        slug=slug,
    )

    ensure_can_edit_discipline(
        user=request.user,
        discipline=discipline,
    )

    if request.method == "POST":
        form = DisciplineForm(
            request.POST,
            instance=discipline,
        )

        if form.is_valid():
            discipline = update_discipline(
                form=form,
            )

            messages.success(
                request,
                "Изменения успешно сохранены.",
            )

            return redirect(
                "courses:discipline_detail",
                slug=discipline.slug,
            )

        else:
            messages.error(
                request,
                "Не удалось сохранить изменения. "
                "Проверьте введённые данные.",
            )

    else:
        form = DisciplineForm(
            instance=discipline,
        )

    context = {
        "form": form,
        "discipline": discipline,
        "page_title": "Редактирование дисциплины",
        "button_text": "Сохранить изменения",
    }

    return render(
        request,
        "courses/discipline_form.html",
        context,
    )
def topic_detail(
    request,
    discipline_slug,
    topic_slug,
):
    topic = get_object_or_404(
        Topic.objects.select_related(
            "discipline",
            "discipline__created_by",
        ),
        discipline__slug=discipline_slug,
        slug=topic_slug,
    )

    context = {
        "topic": topic,
        "discipline": topic.discipline,
        "can_edit": can_edit_topic(
            user=request.user,
            topic=topic,
        ),
    }

    return render(
        request,
        "courses/topic_detail.html",
        context,
    )


@login_required
def topic_create(
    request,
    discipline_slug,
):
    discipline = get_object_or_404(
        Discipline,
        slug=discipline_slug,
    )

    ensure_can_edit_discipline(
        user=request.user,
        discipline=discipline,
    )

    if request.method == "POST":
        form = TopicForm(
            request.POST,
            discipline=discipline,
        )

        if form.is_valid():
            topic = create_topic(
                form=form,
                discipline=discipline,
            )

            messages.success(
                request,
                "Тема успешно создана.",
            )

            return redirect(
                "courses:topic_detail",
                discipline_slug=discipline.slug,
                topic_slug=topic.slug,
            )

        messages.error(
            request,
            "Не удалось создать тему. "
            "Проверьте введённые данные.",
        )

    else:
        form = TopicForm(
            discipline=discipline,
        )

    context = {
        "form": form,
        "discipline": discipline,
        "page_title": "Создание темы",
        "button_text": "Создать тему",
    }

    return render(
        request,
        "courses/topic_form.html",
        context,
    )


@login_required
def topic_edit(
    request,
    discipline_slug,
    topic_slug,
):
    topic = get_object_or_404(
        Topic.objects.select_related(
            "discipline"
        ),
        discipline__slug=discipline_slug,
        slug=topic_slug,
    )

    ensure_can_edit_topic(
        user=request.user,
        topic=topic,
    )

    if request.method == "POST":
        form = TopicForm(
            request.POST,
            instance=topic,
            discipline=topic.discipline,
        )

        if form.is_valid():
            topic = update_topic(
                form=form,
            )

            messages.success(
                request,
                "Изменения темы успешно сохранены.",
            )

            return redirect(
                "courses:topic_detail",
                discipline_slug=(
                    topic.discipline.slug
                ),
                topic_slug=topic.slug,
            )

        messages.error(
            request,
            "Не удалось сохранить изменения. "
            "Проверьте введённые данные.",
        )

    else:
        form = TopicForm(
            instance=topic,
            discipline=topic.discipline,
        )

    context = {
        "form": form,
        "topic": topic,
        "discipline": topic.discipline,
        "page_title": "Редактирование темы",
        "button_text": "Сохранить изменения",
    }

    return render(
        request,
        "courses/topic_form.html",
        context,
    )
