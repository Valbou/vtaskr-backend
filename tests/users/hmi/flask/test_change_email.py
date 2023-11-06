from src.users import RequestChange, RequestType, User
from src.users.persistence import RequestChangeDB, UserDB
from tests.base_test import BaseTestCase

URL_API = "/api/v1"


class TestUserV1ChangeEmail(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.request_change_db = RequestChangeDB()
        self.new_email = self.generate_email()
        self.headers = self.get_json_headers()

    def test_change_email(self):
        headers = self.get_token_headers()
        user_data = {"new_email": self.new_email}
        response = self.client.post(
            f"{URL_API}/users/me/change-email", json=user_data, headers=headers
        )
        self.assertEqual(response.status_code, 200)
        with self.app.sql.get_session() as session:
            request_change = self.request_change_db.find_request(
                session, self.user.email
            )
            self.assertIsInstance(request_change, RequestChange)
            self.assertEqual(request_change.request_type, RequestType.EMAIL)

    def test_change_invalid_email(self):
        headers = self.get_token_headers()
        user_data = {"new_email": self.fake.word()}
        response = self.client.post(
            f"{URL_API}/users/me/change-email", json=user_data, headers=headers
        )
        self.assertEqual(response.status_code, 400)

    def test_change_email_without_token(self):
        user_data = {"new_email": self.new_email}
        response = self.client.post(
            f"{URL_API}/users/me/change-email", json=user_data, headers=self.headers
        )
        self.assertEqual(response.status_code, 401)

    def test_no_get(self):
        response = self.client.get(
            f"{URL_API}/users/me/change-email", headers=self.headers
        )
        self.assertEqual(response.status_code, 405)

    def test_no_put(self):
        response = self.client.put(
            f"{URL_API}/users/me/change-email", headers=self.headers
        )
        self.assertEqual(response.status_code, 405)

    def test_no_patch(self):
        response = self.client.patch(
            f"{URL_API}/users/me/change-email", headers=self.headers
        )
        self.assertEqual(response.status_code, 405)

    def test_no_delete(self):
        response = self.client.delete(
            f"{URL_API}/users/me/change-email", headers=self.headers
        )
        self.assertEqual(response.status_code, 405)


class TestUserV1NewEmail(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.headers = self.get_json_headers()
        self.request_change_db = RequestChangeDB()
        self.user_db = UserDB()
        self.new_email = self.generate_email()

    def _create_request_change_email(self) -> RequestChange:
        headers = self.get_token_headers()
        self.old_email = self.user.email
        user_data = {"new_email": self.new_email}
        self.client.post(
            f"{URL_API}/users/me/change-email", json=user_data, headers=headers
        )
        with self.app.sql.get_session() as session:
            return self.request_change_db.find_request(session, self.user.email)

    def test_set_new_email(self):
        request_change = self._create_request_change_email()
        self.assertIsNotNone(request_change)
        self.assertEqual(self.user.email, self.old_email)

        user_data = {
            "old_email": self.old_email,
            "new_email": self.new_email,
            "hash": request_change.gen_hash(),
            "code": request_change.code,
        }
        response = self.client.post(
            f"{URL_API}/new-email", json=user_data, headers=self.headers
        )
        self.assertEqual(response.status_code, 200)
        with self.app.sql.get_session() as session:
            user = self.user_db.find_login(session, self.new_email)
            self.assertIsInstance(user, User)
            self.assertEqual(user.email, self.new_email)

    def test_no_get(self):
        response = self.client.get(f"{URL_API}/new-email", headers=self.headers)
        self.assertEqual(response.status_code, 405)

    def test_no_put(self):
        response = self.client.put(f"{URL_API}/new-email", headers=self.headers)
        self.assertEqual(response.status_code, 405)

    def test_no_patch(self):
        response = self.client.patch(f"{URL_API}/new-email", headers=self.headers)
        self.assertEqual(response.status_code, 405)

    def test_no_delete(self):
        response = self.client.delete(f"{URL_API}/new-email", headers=self.headers)
        self.assertEqual(response.status_code, 405)
