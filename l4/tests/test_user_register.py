import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserRegister(BaseCase):
    def test_create_user_with_existing_email(self):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'vinkotov@example.com',
        }
        response = requests.post("https://playground.learnqa.ru/api/user", data=data)
        print(response.status_code)
        print(response.content)