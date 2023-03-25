from vtasks.base.config import AVAILABLE_LANGUAGES

from tests import BaseTestCase, FlaskTemplateCapture


class TestBaseRoutes(BaseTestCase):
    def test_home_page(self):
        with FlaskTemplateCapture(self.app) as recorder:
            response = self.client.get("/")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, "text/html; charset=utf-8")
            self.assertTemplateUsed("home.html", recorder.get_recorded_templates())

        self.assertIn("<title>vTasks API</title>", response.text)
        self.assertIn("vtasks-logo-light.svg", response.text)

    def test_languages(self):
        response = self.client.get("/languages")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertDictEqual(response.json, AVAILABLE_LANGUAGES)
