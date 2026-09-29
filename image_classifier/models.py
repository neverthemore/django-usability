from django.db import models

from core.fields import JSONListField


class ImagePrediction(models.Model):
    session_key = models.CharField(max_length=40, db_index=True)
    image = models.ImageField(upload_to="predictions/%Y/%m/%d")
    labels = JSONListField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "классификация изображения"
        verbose_name_plural = "классификации изображений"

    def __str__(self):
        return self.image.name
