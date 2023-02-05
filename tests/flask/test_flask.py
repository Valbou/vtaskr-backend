from tests.base_http_test import FlaskTestCase, FlaskTemplateCapture


class TestFlask(FlaskTestCase):
    def test_home_page(self):
        recorder = FlaskTemplateCapture(self.app)
        with recorder:
            response = self.client.get("/")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, "text/html; charset=utf-8")
            self.assertTemplateUsed("home.html", recorder.get_recorded_templates())

        self.assertIn("<title>vTask API</title>", response.text)
        self.assertIn("vtasks-logo-light.svg", response.text)
