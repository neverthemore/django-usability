from django import forms
from PIL import Image, UnidentifiedImageError

from .models import ImagePrediction


MAX_IMAGE_SIZE = 5 * 1024 * 1024
ALLOWED_FORMATS = {"JPEG", "PNG", "WEBP"}


class ImagePredictionForm(forms.ModelForm):
    class Meta:
        model = ImagePrediction
        fields = ["image"]
        labels = {"image": "Изображение"}
        help_texts = {"image": "JPEG, PNG или WebP, не более 5 МБ."}
        widgets = {
            "image": forms.ClearableFileInput(
                attrs={"accept": "image/jpeg,image/png,image/webp", "data-image-input": "true"}
            )
        }

    def clean_image(self):
        uploaded = self.cleaned_data["image"]
        if uploaded.size > MAX_IMAGE_SIZE:
            raise forms.ValidationError("Файл больше 5 МБ.")
        try:
            uploaded.seek(0)
            with Image.open(uploaded) as image:
                image_format = image.format
                image.verify()
            uploaded.seek(0)
        except (UnidentifiedImageError, OSError, ValueError) as exc:
            raise forms.ValidationError("Файл не является корректным изображением.") from exc
        if image_format not in ALLOWED_FORMATS:
            raise forms.ValidationError("Поддерживаются только JPEG, PNG и WebP.")
        return uploaded

