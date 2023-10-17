from tests.base_test import BaseTestCase, FlaskTemplateCapture
from vtaskr.base.config import AVAILABLE_LANGUAGES


class TestBaseRoutes(BaseTestCase):
    def test_home_page(self):
        with FlaskTemplateCapture(self.app) as recorder:
            response = self.client.get("/")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, "text/html; charset=utf-8")
            self.assertTemplateUsed("home.html", recorder.get_recorded_templates())

        self.assertIn("<title>vTaskr API</title>", response.text)
        self.assertIn("vtaskr-logo-light.svg", response.text)

    def test_languages(self):
        response = self.client.get("/languages")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertDictEqual(response.json, AVAILABLE_LANGUAGES)

    def test_api_documentation(self):
        response = self.client.get("/documentation")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertIn('"openapi": "3.1.0"', response.text)
