from django.contrib import admin

from .models import RequestLog


@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    """Admin interface for RequestLog model."""

    list_display = [
        "id",
        "user",
        "method",
        "smiles_preview",
        "image_format",
        "success",
        "response_time_ms",
        "created_at",
    ]
    list_filter = [
        "method",
        "success",
        "image_format",
        "user",
        "created_at",
    ]
    search_fields = [
        "smiles",
        "user_agent",
        "user__username",
    ]
    readonly_fields = [
        "user",
        "method",
        "smiles",
        "has_molfile",
        "width",
        "height",
        "image_format",
        "success",
        "error_message",
        "response_time_ms",
        "user_agent",
        "created_at",
    ]
    date_hierarchy = "created_at"
    ordering = ["-created_at"]

    @admin.display(description="SMILES")
    def smiles_preview(self, obj):
        """Show truncated SMILES string."""
        if obj.smiles:
            return obj.smiles[:30] + "..." if len(obj.smiles) > 30 else obj.smiles
        return "-"

    def has_add_permission(self, request):
        """Disable manual creation of logs."""
        return False
