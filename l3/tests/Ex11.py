import requests
class TestCheckCookie:
    def test_print_cookie_and_check(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        print(response.cookies)
        assert response.cookies, f"Response has no cookies"
        assert 'HomeWork' in response.cookies, f"Response has no cookie with name HomeWork"
        assert response.cookies['HomeWork'] == 'hw_value', f"Response cookie HomeWork has value '{response.cookies['HomeWork']}'"
