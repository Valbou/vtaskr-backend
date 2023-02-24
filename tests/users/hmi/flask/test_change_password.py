from tests import BaseTestCase

from vtasks.users import RequestChange, RequestType
from vtasks.users.persistence import RequestChangeDB


URL_API = "/api/v1"


class TestUserV1ForgottenPassword(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.request_change_db = RequestChangeDB()
        self.headers = self.get_json_headers()

    def test_forgotten_password(self):
        self.create_user()
        user_data = {"email": self.user.email}
        response = self.client.post(
            f"{URL_API}/forgotten-password", json=user_data, headers=self.headers
        )
        self.assertEqual(response.status_code, 200)
        with self.app.sql_service.get_session() as session:
            request_change = self.request_change_db.find_request(
                session, self.user.email
            )
            self.assertIsInstance(request_change, RequestChange)
            self.assertEqual(request_change.request_type, RequestType.PASSWORD)

    def test_forgotten_password_unknown_email(self):
        self.create_user()
        user_data = {"email": self.fake.email(domain="valbou.fr")}
        response = self.client.post(
            f"{URL_API}/forgotten-password", json=user_data, headers=self.headers
        )
        self.assertEqual(response.status_code, 200)
        with self.app.sql_service.get_session() as session:
            request_change = self.request_change_db.find_request(
                session, self.user.email
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
        self.request_change_db = RequestChangeDB()
        self.headers = self.get_json_headers()

    def _create_request_change_password(self) -> RequestChange:
        self.create_user()
        user_data = {"email": self.user.email}
        self.client.post(
            f"{URL_API}/forgotten-password", json=user_data, headers=self.headers
        )
        with self.app.sql_service.get_session() as session:
            return self.request_change_db.find_request(session, self.user.email)

    def test_set_new_password(self):
        request_change = self._create_request_change_password()
        self.assertIsNotNone(request_change)
        new_password = self.fake.bothify("??? ###??? ###")
        self.assertFalse(self.user.check_password(new_password))
        user_data = {
            "email": self.user.email,
            "hash": request_change.gen_hash(),
            "new_password": new_password,
        }
        response = self.client.post(
            f"{URL_API}/new-password", json=user_data, headers=self.headers
        )
        self.assertEqual(response.status_code, 200)
        with self.app.sql_service.get_session() as session:
            user = self.user_db.find_login(session, self.user.email)
            self.assertTrue(user.check_password(new_password))

    def test_set_new_password_bad_hash(self):
        self.create_user()
        new_password = self.fake.bothify("??? ###??? ###")
        user_data = {
            "email": self.user.email,
            "hash": self.fake.word(),
            "new_password": new_password,
        }
        response = self.client.post(
            f"{URL_API}/new-password", json=user_data, headers=self.headers
        )
        self.assertEqual(response.status_code, 400)

    def test_set_new_password_bad_email(self):
        request_change = self._create_request_change_password()
        new_password = self.fake.bothify("??? ###??? ###")
        user_data = {
            "email": self.fake.email(domain="valbou.fr"),
            "hash": request_change.gen_hash(),
            "new_password": new_password,
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
