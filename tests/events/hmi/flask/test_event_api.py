from unittest.mock import MagicMock, patch

from src.events.models import Event
from tests.base_test import DummyBaseTestCase, set_fake_authentication

URL_API = "/api/v1"

USER_EVENT = Event(
    tenant_id="tenant_123", name="Test Event", data={"title": "Event Title"}
)


class TestEventAPI(DummyBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.headers = self.get_json_headers()

    def test_get_event_no_login(self):
        response = self.client.get(
            f"{URL_API}/events/events/{USER_EVENT.tenant_id}", headers=self.headers
        )
        self.assertEqual(response.status_code, 401)

    @patch(
        "src.events.services.EventsService.get_all_tenant_events",
        return_value=[USER_EVENT],
    )
    def test_get_tenant_events(self, mock_events: MagicMock):
        headers = self.get_token_headers()

        with set_fake_authentication(app=self.app, user=self.user, token=self.token):
            response = self.client.get(
                f"{URL_API}/events/events/{USER_EVENT.tenant_id}", headers=headers
            )

        self.assertEqual(response.status_code, 200)

        mock_events.assert_called_once()
