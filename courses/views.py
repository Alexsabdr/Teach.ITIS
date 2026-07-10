from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.services import (
    ensure_can_manage_disciplines,
)

from .forms import DisciplineForm
from .models import Discipline

def discipline_list(request):
    disciplines = (
        Discipline.objects
        .select_related("created_by")
        .all()
    )

    context = {
        "disciplines": disciplines,
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
            discipline = form.save(commit=False)

            discipline.created_by = request.user

            discipline.save()

            return redirect(
                "courses:discipline_detail",
                slug=discipline.slug,
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

    if request.method == "POST":
        form = DisciplineForm(
            request.POST,
            instance=discipline,
        )

        if form.is_valid():
            discipline = form.save()

            return redirect(
                "courses:discipline_detail",
                slug=discipline.slug,
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

