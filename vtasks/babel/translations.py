import os
from typing import List, Union

from gettext import translation, GNUTranslations

from vtasks.base.config import APP_NAME


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
        return translation(self.domain, self.path, languages=[self.lang,])

    def __exit__(self, exc_type, exc_value, traceback):
        pass


class TranslationService:
    def __init__(self):
        self.domains: list = []
        self.languages: list = []
        self.dirname: str = "translations"

    def _check_valid_domain(self, domain: str):
        if domain not in self.domains:
            raise TranslationsInvalidDomainError(f"The domain {domain} is not installed")

    def _check_valid_language(self, lang: str):
        if lang not in self.languages:
            raise TranslationsInvalidLanguageError(f"The language {lang} is not installed")

    def _path_to_translations(self, domain: str):
        self._check_valid_domain(domain)
        return os.path.join(APP_NAME, domain, self.dirname)

    def get_translation_session(self, domain: str, lang: str):
        self._check_valid_language(lang)
        return TranslationSession(domain, lang, self._path_to_translations(domain))

    def get_translation(self, domain: str, lang: str) -> GNUTranslations:
        self._check_valid_language(lang)
        return translation(domain, self._path_to_translations(domain), languages=[lang,])

    def jinja_install_translation(self, jinja_env, translation: GNUTranslations):
        jinja_env.install_gettext_translations(translation)

    def add_languages(self, languages: Union[List[str], str]):
        if isinstance(languages, str):
            languages = [languages]
        self.languages.extend(languages)

    def add_domains(self, domains: Union[List[str], str]):
        if isinstance(domains, str):
            domains = [domains]
        self.domains.extend(domains)
