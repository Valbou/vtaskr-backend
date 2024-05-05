from abc import ABC, abstractmethod
from gettext import GNUTranslations
from typing import ContextManager

from .base_port import InjectablePort


class TranslationPort(InjectablePort, ABC):
    @abstractmethod
    def get_translation_session(self, domain: str, locale: str) -> ContextManager:
        raise NotImplementedError

    @abstractmethod
    def get_translation(self, domain: str, locale: str) -> GNUTranslations:
        raise NotImplementedError

    @abstractmethod
    def add_languages(self, languages: list[str] | str):
        raise NotImplementedError

    @abstractmethod
    def add_domains(self, domains: list[str] | str):
        raise NotImplementedError
