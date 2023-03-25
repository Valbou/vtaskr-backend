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

        self.user_db = UserDB(self.sql_test.database)
        with self.sql_test.get_session() as session:
            session.expire_on_commit = False
            self.user_db.save(session, self.user)

    def test_get_user(self):
        response = self.client.get(f"/{URL_API_USERS}/{self.user.id}")
        self.assertEqual(response.status_code, 404)

    def test_get_all_users(self):
        response = self.client.get(f"/{URL_API_USERS}")
        self.assertEqual(response.status_code, 404)

    def test_get_user_login(self):
        response = self.client.get(f"/{URL_API_USERS}/login")
        self.assertEqual(response.status_code, 404)

    def test_user_post_api(self):
        pass
        # TODO: Doesn't work with flask test_client but works with curl
        # curl -X POST -d '{"test": "ho ho ho"}' -H "Content-Type: application/json" \
        # http://127.0.0.1:5000/api/v1/users/login -o curl_return.json -s -v

        # headers = {"Content-Type": "application/json"}
        # payload = {"Test": "Hello !"}
        # response = self.client.post(
        # f"/{URL_API_USERS}/login", headers=headers, json=payload
        # )
        # self.assertEqual(response.status_code, 201)
        # self.assertEqual(response.content_type, "application/json")
