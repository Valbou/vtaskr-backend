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
        response = self.client.get(f"{URL_API_USERS}/{self.user.id}")
        self.assertEqual(response.status_code, 404)

    def test_get_all_users(self):
        response = self.client.get(f"{URL_API_USERS}")
        self.assertEqual(response.status_code, 404)

    def test_get_user_login(self):
        response = self.client.get(f"{URL_API_USERS}/login")
        self.assertEqual(response.status_code, 405)

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

    def test_post_login_unknown_user(self):
        headers = {"Content-Type": "application/json"}
        payload = {
            "email": self.fake.email(domain="valbou.fr"),
            "password": self.fake.password(),
        }
        response = self.client.post(
            f"{URL_API_USERS}/login", headers=headers, json=payload
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(
            response.text, '{"error": "Invalid credentials", "status": 401}'
        )

    def test_post_login_known_user_bad_password(self):
        headers = {"Content-Type": "application/json"}
        payload = {
            "email": self.user.email,
            "password": self.fake.password(),
        }
        response = self.client.post(
            f"{URL_API_USERS}/login", headers=headers, json=payload
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(
            response.text, '{"error": "Invalid credentials", "status": 401}'
        )

    def test_delete_logout(self):
        token = self.get_token()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        payload = {"email": self.user.email}
        response = self.client.delete(
            f"{URL_API_USERS}/logout", headers=headers, json=payload
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.text, "")

    def test_delete_logout_unknown_email(self):
        token = self.get_token()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        payload = {"email": self.fake.email(domain="valbou.fr")}
        response = self.client.delete(
            f"{URL_API_USERS}/logout", headers=headers, json=payload
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.text, '{"error": "Unauthorized", "status": 403}')

    def test_get_me(self):
        token = self.get_token()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        response = self.client.get(f"{URL_API_USERS}/me", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.json.get("first_name"), self.user.first_name)
        self.assertEqual(response.json.get("last_name"), self.user.last_name)
        self.assertEqual(response.json.get("email"), self.user.email)

    def test_put_user(self):
        new_first_name = self.fake.first_name()
        token = self.get_token()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        payload = {"first_name": new_first_name}
        response = self.client.put(
            f"{URL_API_USERS}/me/update", headers=headers, json=payload
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.json.get("first_name"), new_first_name)
        self.assertEqual(response.json.get("last_name"), self.user.last_name)

    def test_patch_user(self):
        new_last_name = self.fake.last_name()
        token = self.get_token()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        payload = {"last_name": new_last_name}
        response = self.client.patch(
            f"{URL_API_USERS}/me/update", headers=headers, json=payload
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.json.get("first_name"), self.user.first_name)
        self.assertEqual(response.json.get("last_name"), new_last_name)
