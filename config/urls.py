from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),

    path(
        "accounts/",
        include("accounts.urls"),
    ),

    path(
        "courses/",
        include("courses.urls"),
    ),
]
handler404 = (
    "config.error_handlers.page_not_found"
)

handler403 = (
    "config.error_handlers.permission_denied"
)