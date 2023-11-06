import os
from gettext import GNUTranslations, translation

from babel import Locale


class TranslationsInvalidDomainError(Exception):
    pass


class TranslationsInvalidLanguageError(Exception):
    pass


class TranslationSession:
    def __init__(self, domain: str, lang: str, path: str) -> None:
        self.domain = domain
        self.lang = lang
        self.path = path

    def __enter__(self) -> GNUTranslations:
        return translation(
            self.domain,
            self.path,
            languages=[
                self.lang,
            ],
        )

    def __exit__(self, exc_type, exc_value, traceback):
        pass


class TranslationService:
    def __init__(self):
        self.domains: list = []
        self.languages: list = []
        self.dirname: str = "translations"

    def _check_valid_domain(self, domain: str):
        if domain not in self.domains:
            raise TranslationsInvalidDomainError(
                f"The domain {domain} is not installed"
            )

    def _check_valid_language(self, lang: str):
        if lang not in self.languages:
            raise TranslationsInvalidLanguageError(
                f"The language {lang} is not installed"
            )

    def _locale_to_lang(self, locale: Locale | str) -> str:
        if isinstance(locale, str):
            locale = Locale.parse(locale)
        return locale.language

    def _path_to_translations(self, domain: str):
        self._check_valid_domain(domain)
        return os.path.join("src", domain, self.dirname)

    def get_translation_session(self, domain: str, locale: Locale | str):
        lang = self._locale_to_lang(locale)
        self._check_valid_language(lang)
        return TranslationSession(domain, lang, self._path_to_translations(domain))

    def get_translation(self, domain: str, locale: Locale | str) -> GNUTranslations:
        lang = self._locale_to_lang(locale)
        self._check_valid_language(lang)
        return translation(
            domain,
            self._path_to_translations(domain),
            languages=[
                lang,
            ],
        )

    def jinja_install_translation(self, jinja_env, translation: GNUTranslations):
        jinja_env.install_gettext_translations(translation)

    def add_languages(self, languages: list[str] | str):
        if isinstance(languages, str):
            languages = [languages]
        self.languages.extend(languages)

    def add_domains(self, domains: list[str] | str):
        if isinstance(domains, str):
            domains = [domains]
        self.domains.extend(domains)
