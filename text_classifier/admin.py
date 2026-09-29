from django.contrib import admin

from .models import TextAnalysis


@admin.register(TextAnalysis)
class TextAnalysisAdmin(admin.ModelAdmin):
    list_display = ("short_text", "created_at")
    readonly_fields = ("session_key", "scores", "created_at")

    @admin.display(description="Текст")
    def short_text(self, obj):
        return obj.text[:80]

