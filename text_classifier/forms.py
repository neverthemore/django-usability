from django import forms

from .models import TextAnalysis


class TextAnalysisForm(forms.ModelForm):
    class Meta:
        model = TextAnalysis
        fields = ["text"]
        labels = {"text": "Текст для анализа"}
        help_texts = {"text": "До 500 символов. Оценки эмоций независимы и не обязаны давать 100% в сумме."}
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "rows": 5,
                    "maxlength": 500,
                    "placeholder": "Например: Я очень рад нашей встрече!",
                    "data-character-counter": "text-counter",
                }
            )
        }

