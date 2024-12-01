from gettext import GNUTranslations, NullTranslations
from unittest import TestCase

from src.libs.babel.translations import (
    TranslationService,
    TranslationSession,
    TranslationsInvalidDomainError,
    TranslationsInvalidLanguageError,
)


class TestTranslationService(TestCase):
    def setUp(self):
        super().setUp()
        self.translation = TranslationService()

    def test_valid_domain(self):
        self.translation.add_domains(["domain", "messages"])
        self.assertIsNone(self.translation._check_valid_domain("domain"))
        self.assertIsNone(self.translation._check_valid_domain("messages"))

        with self.assertRaises(TranslationsInvalidDomainError):
            self.translation._check_valid_domain("test")

    def test_valid_lang(self):
        self.translation.add_languages(["fr", "en"])
        self.assertIsNone(self.translation._check_valid_language("fr"))
        self.assertIsNone(self.translation._check_valid_language("en"))

        with self.assertRaises(TranslationsInvalidLanguageError):
            self.translation._check_valid_language("de")

    def test_path_to_translations(self):
        self.translation.add_domains("test")
        self.assertEqual(
            self.translation._path_to_translations("test"), "src/test/translations"
        )

    def test_get_translation(self):
        self.translation.add_domains(["test", "notifications"])
        self.translation.add_languages(["fr", "ja"])

        with self.assertRaises(FileNotFoundError):
            self.translation.get_translation("test", "fr")

        with self.assertRaises(FileNotFoundError):
            self.translation.get_translation("notifications", "ja")

        self.assertIsInstance(
            self.translation.get_translation("notifications", "fr"), GNUTranslations
        )

    def test_get_translation_session(self):
        self.translation.add_domains("notifications")
        self.translation.add_languages("fr")
        self.assertIsInstance(
            self.translation.get_translation_session("notifications", "fr"),
            TranslationSession,
        )


class TestTranslationSession(TestCase):
    def setUp(self):
        super().setUp()
        self.trans = TranslationSession(
            domain="notifications", lang="fr", path="src/notifications/translations"
        )

    def test_trans_session(self):
        with self.trans as trans:
            self.assertIsInstance(trans, (GNUTranslations, NullTranslations))
            self.assertEqual(trans.gettext("test"), "test")
