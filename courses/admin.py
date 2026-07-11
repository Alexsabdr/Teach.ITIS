from django.contrib import admin

from .models import Discipline, Topic, Enrollment


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "slug",
        "created_by",
        "created_at",
    )

    search_fields = (
        "title",
        "slug",
        "description",
    )

    list_filter = (
        "created_at",
    )


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "discipline",
        "order_number",
        "created_at",
    )

    search_fields = (
        "title",
        "slug",
        "description",
        "discipline__title",
    )

    list_filter = (
        "discipline",
        "created_at",
    )


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "discipline",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
        "discipline__title",
    )

    list_filter = (
        "discipline",
        "created_at",
    )