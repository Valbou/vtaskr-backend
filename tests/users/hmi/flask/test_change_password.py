from src.users.models import RequestChange, RequestType
from src.users.persistence import RequestChangeDBPort, UserDBPort
from src.users.settings import APP_NAME
from tests.base_test import BaseTestCase

URL_API = "/api/v1"


class TestUserV1ForgottenPassword(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.request_change_db: RequestChangeDBPort = (
            self.app.dependencies.persistence.get_repository(APP_NAME, "RequestChange")
        )
        self.headers = self.get_json_headers()

    def test_forgotten_password(self):
        self.create_user()
        user_data = {"email": self.user.email}
        response = self.client.post(
            f"{URL_API}/forgotten-password", json=user_data, headers=self.headers
        )
        self.assertEqual(response.status_code, 200)
        with self.app.dependencies.persistence.get_session() as session:
            request_change = self.request_change_db.find_request(
                session, self.user.email, RequestType.PASSWORD
            )
            self.assertIsInstance(request_change, RequestChange)
            self.assertEqual(request_change.request_type, RequestType.PASSWORD)

    def test_forgotten_password_unknown_email(self):
        self.create_user()
        user_data = {"email": self.generate_email()}
        response = self.client.post(
            f"{URL_API}/forgotten-password", json=user_data, headers=self.headers
        )
        self.assertEqual(response.status_code, 200)
        with self.app.dependencies.persistence.get_session() as session:
            request_change = self.request_change_db.find_request(
                session, self.user.email, RequestType.PASSWORD
            )
            self.assertIsNone(request_change)

    def test_no_get(self):
        response = self.client.get(
            f"{URL_API}/forgotten-password", headers=self.headers
        )
        self.assertEqual(response.status_code, 405)

    def test_no_put(self):
        response = self.client.put(
            f"{URL_API}/forgotten-password", headers=self.headers
        )
        self.assertEqual(response.status_code, 405)

    def test_no_patch(self):
        response = self.client.patch(
            f"{URL_API}/forgotten-password", headers=self.headers
        )
        self.assertEqual(response.status_code, 405)

    def test_no_delete(self):
        response = self.client.delete(
            f"{URL_API}/forgotten-password", headers=self.headers
        )
        self.assertEqual(response.status_code, 405)


class TestUserV1NewPassword(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.request_change_db: RequestChangeDBPort = (
            self.app.dependencies.persistence.get_repository(APP_NAME, "RequestChange")
        )
        self.user_db: UserDBPort = self.app.dependencies.persistence.get_repository(
            APP_NAME, "User"
        )
        self.headers = self.get_json_headers()
        self.new_password = self.generate_password()

    def _create_request_change_password(self) -> RequestChange:
        self.create_user()
        user_data = {"email": self.user.email}
        self.client.post(
            f"{URL_API}/forgotten-password", json=user_data, headers=self.headers
        )
        with self.app.dependencies.persistence.get_session() as session:
            return self.request_change_db.find_request(
                session, self.user.email, RequestType.PASSWORD
            )

    def test_set_new_password(self):
        request_change = self._create_request_change_password()
        self.assertIsNotNone(request_change)
        self.assertFalse(self.user.check_password(self.new_password))
        user_data = {
            "email": self.user.email,
            "hash": request_change.gen_hash(),
            "new_password": self.new_password,
        }
        response = self.client.post(
            f"{URL_API}/new-password", json=user_data, headers=self.headers
        )
        self.assertEqual(response.status_code, 200)
        with self.app.dependencies.persistence.get_session() as session:
            user = self.user_db.find_user_by_email(session, self.user.email)
            self.assertTrue(user.check_password(self.new_password))

    def test_set_new_password_bad_hash(self):
        self.create_user()
        user_data = {
            "email": self.user.email,
            "hash": self.fake.word(),
            "new_password": self.new_password,
        }
        response = self.client.post(
            f"{URL_API}/new-password", json=user_data, headers=self.headers
        )
        self.assertEqual(response.status_code, 400)

    def test_set_new_password_bad_email(self):
        request_change = self._create_request_change_password()
        user_data = {
            "email": self.generate_email(),
            "hash": request_change.gen_hash(),
            "new_password": self.new_password,
        }
        response = self.client.post(
            f"{URL_API}/new-password", json=user_data, headers=self.headers
        )
        self.assertEqual(response.status_code, 400)

    def test_no_get(self):
        response = self.client.get(f"{URL_API}/new-password", headers=self.headers)
        self.assertEqual(response.status_code, 405)

    def test_no_put(self):
        response = self.client.put(f"{URL_API}/new-password", headers=self.headers)
        self.assertEqual(response.status_code, 405)

    def test_no_patch(self):
        response = self.client.patch(f"{URL_API}/new-password", headers=self.headers)
        self.assertEqual(response.status_code, 405)

    def test_no_delete(self):
        response = self.client.delete(f"{URL_API}/new-password", headers=self.headers)
        self.assertEqual(response.status_code, 405)
