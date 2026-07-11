from django.urls import path

from . import views


app_name = "courses"


urlpatterns = [
    path(
        "",
        views.discipline_list,
        name="discipline_list",
    ),

    path(
        "create/",
        views.discipline_create,
        name="discipline_create",
    ),

    path(
        "<slug:slug>/edit/",
        views.discipline_edit,
        name="discipline_edit",
    ),

    path(
        "<slug:slug>/",
        views.discipline_detail,
        name="discipline_detail",
    ),
]