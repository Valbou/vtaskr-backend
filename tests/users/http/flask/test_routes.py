from tests import BaseTestCase

from vtasks.users import User
from vtasks.users.persistence import UserDB


URL_API_USERS = "/api/v1/users"


class TestUserV1Routes(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.password = self.fake.password()
        self.user = User(
            first_name=self.fake.first_name(),
            last_name=self.fake.last_name(),
            email=self.fake.email(domain="valbou.fr"),
        )
        self.user.set_password(self.password)

        self.user_db = UserDB()
        with self.app.sql_service.get_session() as session:
            session.expire_on_commit = False
            self.user_db.save(session, self.user)

    def get_token(self) -> str:
        headers = {"Content-Type": "application/json"}
        payload = {
            "email": self.user.email,
            "password": self.password,
        }
        response = self.client.post(
            f"{URL_API_USERS}/login", headers=headers, json=payload
        )
        return response.json.get("token")

    def test_get_user(self):
        response = self.client.get(f"/{URL_API_USERS}/{self.user.id}")
        self.assertEqual(response.status_code, 404)

    def test_get_all_users(self):
        response = self.client.get(f"/{URL_API_USERS}")
        self.assertEqual(response.status_code, 404)

    def test_get_user_login(self):
        response = self.client.get(f"/{URL_API_USERS}/login")
        self.assertEqual(response.status_code, 404)

    def test_post_login(self):
        headers = {"Content-Type": "application/json"}
        payload = {
            "email": self.user.email,
            "password": self.password,
        }
        response = self.client.post(
            f"{URL_API_USERS}/login", headers=headers, json=payload
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content_type, "application/json")
        token = response.json.get("token")
        self.assertEqual(len(token), 64)

    def test_delete_logout(self):
        token = self.get_token()
        headers = {"Content-Type": "application/json"}
        payload = {
            "email": self.user.email,
            "token": token,
        }
        response = self.client.delete(
            f"{URL_API_USERS}/logout", headers=headers, json=payload
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.text, "")
