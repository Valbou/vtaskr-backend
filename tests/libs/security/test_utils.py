from unittest import TestCase

from src.libs.security.utils import file_to_base64


class TestFileBase64(TestCase):
    def test_file_to_base64(self):
        expected = (
            "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9Im5vIj8"
        )
        file_name = "src/static/vtaskr-logo-light.svg"
        result = file_to_base64(file_name)
        self.assertIn(expected, result)
        self.assertTrue(result.startswith(expected))
