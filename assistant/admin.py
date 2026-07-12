from django.contrib import admin

from .models import (
    KnowledgeChunk,
    ChatSession,
    ChatMessage,
    ChatMessageSource,
)


@admin.register(KnowledgeChunk)
class KnowledgeChunkAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "material",
        "discipline",
        "chunk_index",
        "created_at",
    )

    search_fields = (
        "content",
        "material__title",
        "discipline__title",
    )

    list_filter = (
        "discipline",
        "created_at",
    )


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "user",
        "discipline",
        "created_at",
    )

    search_fields = (
        "title",
        "user__username",
        "user__email",
        "discipline__title",
    )

    list_filter = (
        "discipline",
        "created_at",
    )


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "session",
        "role",
        "created_at",
    )

    search_fields = (
        "content",
        "session__title",
        "session__user__username",
    )

    list_filter = (
        "role",
        "created_at",
    )


@admin.register(ChatMessageSource)
class ChatMessageSourceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "message",
        "material",
    )

    search_fields = (
        "quote",
        "message__content",
        "material__title",
    )

    list_filter = (
        "material__topic__discipline",
    )