from django.conf import settings
from django.db import models
from django.utils import timezone


class Material(models.Model):
    class MaterialType(models.TextChoices):
        VIDEO = "video", "Video"
        FILE = "file", "File"
        TEXT = "text", "Text"

    topic = models.ForeignKey(
        "courses.Topic",
        on_delete=models.CASCADE,
        related_name="materials",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="authored_materials",
    )
    title = models.CharField(max_length=255)
    material_type = models.CharField(max_length=20, choices=MaterialType.choices)
    description = models.TextField(blank=True)
    video_url = models.URLField(max_length=500, blank=True)
    file_url = models.URLField(max_length=500, blank=True)
    text_content = models.TextField(blank=True)
    duration_seconds = models.PositiveIntegerField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "materials"
        ordering = ["topic", "title"]
        constraints = [
            models.UniqueConstraint(
                fields=["topic", "title"],
                name="unique_material_title_per_topic",
            ),
        ]

    def __str__(self):
        return self.title


class ViewHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="view_history",
    )
    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        related_name="view_history",
    )
    progress_seconds = models.PositiveIntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    last_viewed_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "view_history"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "material"],
                name="unique_view_history_per_user_material",
            ),
        ]

    def __str__(self):
        return f"{self.user} -> {self.material}"
