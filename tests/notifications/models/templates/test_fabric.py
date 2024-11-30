from unittest import TestCase

from src.notifications.models import (
    AbstractTemplate,
    BaseEmailTemplate,
    TemplateFabric,
    UsersRegisterTemplate,
)
from src.notifications.settings import MessageType


class TestFabric(TestCase):
    def test_get_complete_recursive_subclasses(self):
        fab = TemplateFabric()
        templates = fab._get_complete_recursive_subclasses()

        self.assertGreater(len(templates), 3)

    def test_get_template(self):
        fab = TemplateFabric()
        template = fab.get_template(
            template_type=MessageType.EMAIL, name="users:register:user"
        )

        self.assertIsInstance(template, AbstractTemplate)
        self.assertIsInstance(template, BaseEmailTemplate)
        self.assertIsInstance(template, UsersRegisterTemplate)
