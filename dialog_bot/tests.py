from unittest.mock import patch

from django.test import Client, TestCase
from django.urls import reverse

from .models import ChatMessage


class FakeChatPredictor:
    def predict(self, messages):
        return f"Ответ на: {messages[-1]}"


class DialogBotTests(TestCase):
    url = reverse("dialog_bot:index")

    @patch("dialog_bot.views.get_predictor", return_value=FakeChatPredictor())
    def test_post_creates_user_and_assistant_messages(self, mocked_loader):
        response = self.client.post(self.url, {"message": "Привет"})

        self.assertEqual(response.status_code, 302)
        messages = list(ChatMessage.objects.values_list("role", "text"))
        self.assertEqual(
            messages,
            [(ChatMessage.Role.USER, "Привет"), (ChatMessage.Role.ASSISTANT, "Ответ на: Привет")],
        )
        mocked_loader.assert_called_once()

    def test_clear_removes_only_current_session(self):
        self.client.get(self.url)
        first_key = self.client.session.session_key
        other_client = Client()
        other_client.get(self.url)
        other_key = other_client.session.session_key
        ChatMessage.objects.create(session_key=first_key, role="user", text="Первый")
        ChatMessage.objects.create(session_key=other_key, role="user", text="Второй")

        response = self.client.post(reverse("dialog_bot:clear"))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(ChatMessage.objects.filter(session_key=first_key).exists())
        self.assertTrue(ChatMessage.objects.filter(session_key=other_key).exists())

    def test_conversation_is_not_visible_to_other_session(self):
        self.client.get(self.url)
        ChatMessage.objects.create(
            session_key=self.client.session.session_key,
            role="user",
            text="Только для первой сессии",
        )

        response = Client().get(self.url)

        self.assertNotContains(response, "Только для первой сессии")

