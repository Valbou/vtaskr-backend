from datetime import datetime
from typing import Optional
from unittest import TestCase

from faker import Faker
from vtasks.tasks import Color, Tag


class TestTag(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.fake = Faker()
        self.tag = Tag(
            user_id="1234abcd",
            title=self.fake.text(max_nb_chars=50),
        )

    def test_tag_table_fields(self):
        self.assertEqual(Tag.__annotations__.get("id"), str)
        self.assertEqual(Tag.__annotations__.get("title"), str)
        self.assertEqual(Tag.__annotations__.get("user_id"), str)
        self.assertEqual(Tag.__annotations__.get("color"), Optional[Color])
        self.assertEqual(Tag.__annotations__.get("created_at"), Optional[datetime])


class TestColor(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.fake = Faker()
        self.color = Color(
            background=self.fake.hex_color(),
            text=self.fake.hex_color(),
        )

    def test_check_bad_format(self):
        test_formats = [
            "#12345",  # 1 char too short
            "#1234567",  # 1 char too long
            "#abcdeg",  # 1 bad char
            "123456",  # missing: "#"
        ]
        for t in test_formats:
            with self.subTest(t):
                self.assertFalse(Color.check_format(t))

    def test_check_good_format(self):
        test_formats = [
            "#123456",  # only numbers
            "#abcdef",  # only letters
            "#123abc",  # mix number letter
            "#fed987",  # mix number letter
        ]
        for t in test_formats:
            with self.subTest(t):
                self.assertTrue(Color.check_format(t))

    def test_from_string(self):
        color: Color = Color.from_string("#123456|#654321")
        self.assertIsInstance(color, Color)
        self.assertEqual(color.background, "#123456")
        self.assertEqual(color.text, "#654321")
