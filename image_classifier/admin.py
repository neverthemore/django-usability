from django.contrib import admin

from .models import ImagePrediction


@admin.register(ImagePrediction)
class ImagePredictionAdmin(admin.ModelAdmin):
    list_display = ("image", "created_at")
    readonly_fields = ("session_key", "labels", "created_at")

