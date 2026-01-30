from django.conf import settings
from django.db import models


class RequestLog(models.Model):
    """Log of API requests for analytics and monitoring."""

    class Method(models.TextChoices):
        GET = "GET", "GET"
        POST = "POST", "POST"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="request_logs",
        verbose_name="User",
    )
    method = models.CharField(
        max_length=4,
        choices=Method.choices,
        verbose_name="HTTP Method",
    )
    smiles = models.TextField(
        blank=True,
        null=True,
        verbose_name="SMILES String",
    )
    has_molfile = models.BooleanField(
        default=False,
        verbose_name="MOL File Uploaded",
    )
    width = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Image Width",
    )
    height = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Image Height",
    )
    image_format = models.CharField(
        max_length=10,
        blank=True,
        verbose_name="Image Format",
    )
    success = models.BooleanField(
        default=True,
        verbose_name="Request Successful",
    )
    error_message = models.TextField(
        blank=True,
        null=True,
        verbose_name="Error Message",
    )
    response_time_ms = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Response Time (ms)",
    )
    user_agent = models.TextField(
        blank=True,
        null=True,
        verbose_name="User Agent",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At",
        db_index=True,
    )

    class Meta:
        verbose_name = "Request Log"
        verbose_name_plural = "Request Logs"
        ordering = ["-created_at"]

    def __str__(self):
        user_info = getattr(self.user, "username", None) or "Anonymous"
        created = (
            self.created_at.strftime("%Y-%m-%d %H:%M") if self.created_at else "Unknown"
        )
        return f"{self.method} {user_info} - {created}"
