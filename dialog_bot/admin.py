from django.contrib import admin

from .models import ChatMessage


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("role", "short_text", "created_at")
    list_filter = ("role",)
    readonly_fields = ("session_key", "created_at")

    @admin.display(description="Сообщение")
    def short_text(self, obj):
        return obj.text[:80]

