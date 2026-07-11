from django.conf import settings
from django.db import models


class Discipline(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_disciplines",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "disciplines"
        ordering = ["title"]

    def __str__(self):
        return self.title


class Topic(models.Model):
    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.CASCADE,
        related_name="topics",
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True)
    order_number = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "topics"
        ordering = ["discipline", "order_number", "title"]
        constraints = [
            models.UniqueConstraint(
                fields=["discipline", "slug"],
                name="unique_topic_slug_per_discipline",
            ),
            models.UniqueConstraint(
                fields=["discipline", "title"],
                name="unique_topic_title_per_discipline",
            ),
        ]

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )
    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "enrollments"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "discipline"],
                name="unique_enrollment_per_user_discipline",
            ),
        ]

    def __str__(self):
        return f"{self.user} -> {self.discipline}"
