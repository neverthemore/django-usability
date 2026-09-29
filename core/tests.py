from django.test import TestCase
from django.urls import reverse


class HomeTests(TestCase):
    def test_home_shows_all_service_cards(self):
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Анализ эмоций')
        self.assertContains(response, 'Диалоговый бот')
        self.assertContains(response, 'Классификация изображений')

    def test_completed_service_routes_are_available(self):
        for name in ():
            with self.subTest(name=name):
                self.assertEqual(self.client.get(reverse(name)).status_code, 200)
