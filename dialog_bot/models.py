from django.db import models


class ChatMessage(models.Model):
    class Role(models.TextChoices):
        USER = "user", "Пользователь"
        ASSISTANT = "assistant", "Ассистент"

    session_key = models.CharField(max_length=40, db_index=True)
    role = models.CharField(max_length=10, choices=Role.choices)
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name = "сообщение"
        verbose_name_plural = "сообщения"

    def __str__(self):
        return f"{self.get_role_display()}: {self.text[:50]}"

