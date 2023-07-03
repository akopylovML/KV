from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests

class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
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

        # EDIT
        new_name = "Changed Name"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_status_code(response3, 200)

        # GET

        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )
    def test_edit_just_created_user_without_authorization_cookie(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")

        # EDIT
        new_name = "Changed Name"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            data={"firstName": new_name}
        )

        Assertions.assert_status_code(response3, 400)
        assert response3.content.decode("utf-8") == f"Auth token not supplied", \
            f"Unexpected response content {response3.content}"
    def test_edit_just_created_user_with_other_user_auth_data(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email1 = register_data['email']
        password1 = register_data['password']

        # LOGIN
        login_data = {
            'email': email1,
            'password': password1
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # REGISTER2
        register_data = self.prepare_registration_data()
        response3 = MyRequests.post("/user", data=register_data)

        Assertions.assert_status_code(response3, 200)
        Assertions.assert_json_has_key(response3, "id")

        name2 = register_data['firstName']
        email2 = register_data['email']
        password2 = register_data['password']
        user_id2 = self.get_json_value(response3, "id")

        # EDIT user2 with user1 auth data
        new_name = "Changed Name"

        response4 = MyRequests.put(
            f"/user/{user_id2}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_status_code(response4, 200)

        # LOGIN AND GET USER TO CHECK IF NAME CHANGED

        login_data = {
            'email': email2,
            'password': password2
        }
        response5 = MyRequests.post("/user/login", data=login_data)

        auth_sid2 = self.get_cookie(response5, "auth_sid")
        token2 = self.get_header(response5, "x-csrf-token")

        response6 = MyRequests.get(
            f"/user/{user_id2}",
            headers={"x-csrf-token": token2},
            cookies={"auth_sid": auth_sid2},
        )

        Assertions.assert_json_value_by_name(
            response6,
            "firstName",
            name2,
            "User first name was edited by other user"
        )

    def test_edit_just_created_user_with_incorrect_email(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        user_id = self.get_json_value(response1, "id")
        password = register_data['password']

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_email = "testtest.com"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_email}
        )

        Assertions.assert_status_code(response3, 400)
        assert response3.content.decode("utf-8") == f"Invalid email format", \
            f"Unexpected response content {response3.content}"

        # GET

        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_json_value_by_name(
            response4,
            "email",
            email,
            "Email changed unexpectedly"
        )
    def test_edit_just_created_user_with_too_short_name(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        user_id = self.get_json_value(response1, "id")
        password = register_data['password']

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "a"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_status_code(response3, 400)
        assert self.get_json_value(response3, "error") == f"Too short value for field firstName", \
            f"Unexpected response content {response3.content}"