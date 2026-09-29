from unittest.mock import patch

from django.test import Client, TestCase
from django.urls import reverse

from .models import TextAnalysis


class FakePredictor:
    def predict(self, text):
        return [{"label": "Радость", "score": 91.2}]


class TextClassifierTests(TestCase):
    url = reverse("text_classifier:index")

    @patch("text_classifier.views.get_predictor", return_value=FakePredictor())
    def test_valid_post_creates_analysis_and_redirects(self, mocked_loader):
        response = self.client.post(self.url, {"text": "Я рад вас видеть!"})

        self.assertEqual(response.status_code, 302)
        analysis = TextAnalysis.objects.get()
        self.assertEqual(analysis.scores[0]["label"], "Радость")
        self.assertTrue(analysis.session_key)
        self.assertIn(f"result={analysis.pk}", response.url)
        mocked_loader.assert_called_once()

    @patch("text_classifier.views.get_predictor")
    def test_too_long_text_is_rejected_before_model_call(self, mocked_loader):
        response = self.client.post(self.url, {"text": "я" * 501})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(TextAnalysis.objects.count(), 0)
        mocked_loader.assert_not_called()

    def test_history_is_isolated_by_session(self):
        self.client.get(self.url)
        first_key = self.client.session.session_key
        TextAnalysis.objects.create(
            session_key=first_key,
            text="Секретная строка",
            scores=[],
        )

        other_client = Client()
        response = other_client.get(self.url)

        self.assertNotContains(response, "Секретная строка")

    def test_score_bar_uses_locale_independent_integer_width(self):
        self.client.get(self.url)
        analysis = TextAnalysis.objects.create(
            session_key=self.client.session.session_key,
            text="Проверка шкалы",
            scores=[{"label": "Радость", "score": 12.5}],
        )

        response = self.client.get(self.url, {"result": analysis.pk})

        self.assertContains(response, 'style="width: 12%"')
        self.assertNotContains(response, 'style="width: 12,5%"')

