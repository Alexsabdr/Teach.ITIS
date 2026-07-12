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
        "<slug:discipline_slug>/topics/create/",
        views.topic_create,
        name="topic_create",
    ),

    path(
        (
            "<slug:discipline_slug>/"
            "topics/<slug:topic_slug>/edit/"
        ),
        views.topic_edit,
        name="topic_edit",
    ),

    path(
        (
            "<slug:discipline_slug>/"
            "topics/<slug:topic_slug>/"
        ),
        views.topic_detail,
        name="topic_detail",
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