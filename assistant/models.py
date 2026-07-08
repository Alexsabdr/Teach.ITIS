from django.conf import settings
from django.db import models


class KnowledgeChunk(models.Model):
    material = models.ForeignKey(
        "materials.Material",
        on_delete=models.CASCADE,
        related_name="knowledge_chunks",
    )
    discipline = models.ForeignKey(
        "courses.Discipline",
        on_delete=models.CASCADE,
        related_name="knowledge_chunks",
    )
    content = models.TextField()
    chunk_index = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "knowledge_chunks"
        ordering = ["material", "chunk_index"]
        constraints = [
            models.UniqueConstraint(
                fields=["material", "chunk_index"],
                name="unique_chunk_index_per_material",
            ),
        ]

    def __str__(self):
        return f"{self.material} #{self.chunk_index}"


class ChatSession(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chat_sessions",
    )
    discipline = models.ForeignKey(
        "courses.Discipline",
        on_delete=models.CASCADE,
        related_name="chat_sessions",
    )
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "chat_sessions"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class ChatMessage(models.Model):
    class MessageRole(models.TextChoices):
        USER = "user", "User"
        ASSISTANT = "assistant", "Assistant"
        SYSTEM = "system", "System"

    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    role = models.CharField(max_length=20, choices=MessageRole.choices)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "chat_messages"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.role}: {self.content[:50]}"


class ChatMessageSource(models.Model):
    message = models.ForeignKey(
        ChatMessage,
        on_delete=models.CASCADE,
        related_name="sources",
    )
    material = models.ForeignKey(
        "materials.Material",
        on_delete=models.CASCADE,
        related_name="chat_message_sources",
    )
    quote = models.TextField(blank=True)

    class Meta:
        db_table = "chat_message_sources"
        constraints = [
            models.UniqueConstraint(
                fields=["message", "material"],
                name="unique_source_per_message_material",
            ),
        ]

    def __str__(self):
        return f"{self.message_id} -> {self.material_id}"
