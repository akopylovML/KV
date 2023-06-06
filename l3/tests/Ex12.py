import requests
class TestCheckHeader:
    def test_print_header_and_check(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        assert response.headers, f"Response has no headers"
        print(response.headers)
        assert "x-secret-homework-header" in response.headers, f"Response has no x-secret-homework-header header"
        assert response.headers['x-secret-homework-header'] == "Some secret value", \
            f"Header x-secret-homework-header has '{response.headers['x-secret-homework-header']}' value"