import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests

class TestUserRegister(BaseCase):
    def test_create_user_succesfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user", data=data)

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists",\
            f"Unexpected response content {response.content}"
    def test_create_user_with_incorrect_email_format(self):
        email = "incorrectemail.com"
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format",\
            f"Unexpected response content {response.content}"

    creds_to_modify = ("password", "username", "firstName", "lastName", "email")
    @pytest.mark.parametrize('excluded_cred', creds_to_modify)
    def test_create_user_with_incomplete_data_set(self, excluded_cred):
        data = self.prepare_registration_data()
        del data[excluded_cred]
        response = MyRequests.post("/user", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {excluded_cred}", \
            f"Unexpected response content {response.content}"

    incorrect_names_for_registration = ("a", "yW4dCQvqIQPmrqVF2xqxyjq6J8UkHBg5GYQKiZixTDDKqnvpeajt6zQ3UOxQpXcW1RBgX53W4"
                                             "zpwxGR1z4mPlNh052f7sy55OAsJ8ir8SZL3O6KWqICGQscVMSCIHTGjfGpnLskB2VwGORbRuy"
                                             "Jo1Tcxh6PKszTLdwm3Sx4i0iTrwqJPxVyHj6BTBxYGnO8Y0afyGTWKb9tiXEdJehXaTAS1gfi"
                                             "O3PhZb6LjLv6zv3ECHxb7uZW9JOeDcYA")

    @pytest.mark.parametrize('name', incorrect_names_for_registration)
    def test_create_user_with_too_short_name(self, name):
        data = self.prepare_registration_data()
        data["firstName"] = name
        response = MyRequests.post("/user", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'firstName' field is too short" or \
               response.content.decode("utf-8") == f"The value of 'firstName' field is too long", \
            f"Unexpected response content {response.content}"