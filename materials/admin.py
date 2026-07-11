from django.contrib import admin

from .models import Material, ViewHistory


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "material_type",
        "topic",
        "author",
        "is_published",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
        "text_content",
        "topic__title",
        "author__username",
    )

    list_filter = (
        "material_type",
        "is_published",
        "topic__discipline",
        "created_at",
    )


@admin.register(ViewHistory)
class ViewHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "material",
        "progress_seconds",
        "is_completed",
        "last_viewed_at",
    )

    search_fields = (
        "user__username",
        "user__email",
        "material__title",
    )

    list_filter = (
        "is_completed",
        "material__material_type",
        "last_viewed_at",
    )