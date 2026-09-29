from django import forms


class ChatForm(forms.Form):
    message = forms.CharField(
        label="Сообщение",
        max_length=300,
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "maxlength": 300,
                "placeholder": "Напишите короткое сообщение…",
                "data-character-counter": "chat-counter",
            }
        ),
        help_text="До 300 символов. Модель помнит четыре последние реплики.",
    )

