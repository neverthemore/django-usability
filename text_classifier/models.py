from django.db import models

from core.fields import JSONListField


class TextAnalysis(models.Model):
    session_key = models.CharField(max_length=40, db_index=True)
    text = models.TextField(max_length=500)
    scores = JSONListField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "анализ текста"
        verbose_name_plural = "анализы текста"

    def __str__(self):
        return self.text[:60]
