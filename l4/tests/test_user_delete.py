from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserDelete(BaseCase):
    def test_delete_protected_user(self):
        # REGISTER
        user_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        email = user_data['email']
        password = user_data['password']
        user_id = 2

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response1 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # DELETE
        response2 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_status_code(response2, 400)
        assert response2.content.decode("utf-8") == f"Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
            f"Unexpected response content {response2.content}"

    def test_delete_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # DELETE
        response3 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_status_code(response3, 200)

        # GET DELETED USER, RESPONSE CODE SHOULD BE 404
        response4 = MyRequests.get(
            f"/user/{user_id}")

        Assertions.assert_status_code(response4, 404)
    def test_delete_user1_under_user2(self):
        # REGISTER USER1
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email1 = register_data['email']
        password1 = register_data['password']

        # REGISTER USER2
        register_data = self.prepare_registration_data()
        response2 = MyRequests.post("/user", data=register_data)

        Assertions.assert_status_code(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        user_id2 = self.get_json_value(response2, "id")

        # LOGIN
        login_data = {
            'email': email1,
            'password': password1
        }
        response3 = MyRequests.post("/user/login", data=login_data)

        auth_sid1 = self.get_cookie(response3, "auth_sid")
        token1 = self.get_header(response3, "x-csrf-token")

        # DELETE
        response4 = MyRequests.delete(
            f"/user/{user_id2}",
            headers={"x-csrf-token": token1},
            cookies={"auth_sid": auth_sid1}
        )

        Assertions.assert_status_code(response4, 200)

        # GET USER2, CHECK IF IT WAS DELETED
        response5 = MyRequests.get(
            f"/user/{user_id2}")

        Assertions.assert_status_code(response5, 200)

