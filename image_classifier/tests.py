import base64
import tempfile
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from .models import ImagePrediction


PNG_1X1 = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
)


class FakeImagePredictor:
    def predict(self, image_path):
        return [{"label": "tabby", "score": 88.4}]


class ImageClassifierTests(TestCase):
    url = reverse("image_classifier:index")

    def setUp(self):
        self.media_directory = tempfile.TemporaryDirectory()
        self.settings_override = override_settings(MEDIA_ROOT=self.media_directory.name)
        self.settings_override.enable()

    def tearDown(self):
        self.settings_override.disable()
        self.media_directory.cleanup()

    @patch("image_classifier.views.get_predictor", return_value=FakeImagePredictor())
    def test_valid_image_creates_prediction_and_redirects(self, mocked_loader):
        image = SimpleUploadedFile("pixel.png", PNG_1X1, content_type="image/png")

        response = self.client.post(self.url, {"image": image})

        self.assertEqual(response.status_code, 302)
        prediction = ImagePrediction.objects.get()
        self.assertEqual(prediction.labels[0]["label"], "tabby")
        self.assertTrue(prediction.session_key)
        mocked_loader.assert_called_once()

    @patch("image_classifier.views.get_predictor")
    def test_invalid_file_is_rejected_before_model_call(self, mocked_loader):
        fake = SimpleUploadedFile("fake.png", b"not an image", content_type="image/png")

        response = self.client.post(self.url, {"image": fake})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Загрузите правильное изображение")
        self.assertFalse(ImagePrediction.objects.exists())
        mocked_loader.assert_not_called()

    def test_history_is_isolated_by_session(self):
        self.client.get(self.url)
        first_key = self.client.session.session_key
        ImagePrediction.objects.create(
            session_key=first_key,
            image="predictions/private.png",
            labels=[],
        )

        response = Client().get(self.url)

        self.assertNotContains(response, "private.png")

    def test_score_bar_uses_locale_independent_integer_width(self):
        self.client.get(self.url)
        prediction = ImagePrediction.objects.create(
            session_key=self.client.session.session_key,
            image="predictions/example.png",
            labels=[{"label": "tabby", "score": 12.5}],
        )

        response = self.client.get(self.url, {"result": prediction.pk})

        self.assertContains(response, 'style="width: 12%"')
        self.assertNotContains(response, 'style="width: 12,5%"')

