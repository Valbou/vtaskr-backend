from unittest.mock import MagicMock

from src.users.managers import RequestChangeManager
from src.users.models import RequestChange, RequestType
from tests.base_test import DummyBaseTestCase


class TestRequestChangeManager(DummyBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.request_change_m = RequestChangeManager(services=self.app.dependencies)

    def test_create_request_change(self):
        self.request_change_m.request_change_db.clean_history = MagicMock()
        self.request_change_m.request_change_db.save = MagicMock()

        request_change = self.request_change_m.create_request_change(
            session=None, email="test@example.com", request_type=RequestType.EMAIL
        )

        self.request_change_m.request_change_db.clean_history.assert_called_once()
        self.request_change_m.request_change_db.save.assert_called_once()

        self.assertIsInstance(request_change, RequestChange)
        self.assertEqual(request_change.email, "test@example.com")
        self.assertEqual(request_change.request_type, RequestType.EMAIL)

    def test_get_request(self):
        self.request_change_m.request_change_db.find_request = MagicMock()

        self.request_change_m.get_request(session=None, email="test@example.com")

        self.request_change_m.request_change_db.find_request.assert_called_once_with(
            session=None, email="test@example.com"
        )
