import pytest
import requests
import json.decoder
class TestUserAgent:
    user_agents = [
        ("Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30"
         " (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30", "Mobile", "No", "Android"),
        ("Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)"
         " CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1", "Mobile", "Chrome", "iOS"),
        ("Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)", "Googlebot", "Unknown", "Unknown"),
        ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
         " Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0", "Web", "Chrome", "No"),
        ("Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15"
         " (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1", "Mobile", "No", "iPhone")
    ]
    @pytest.mark.parametrize('agent, platform, browser, device', user_agents)
    def test_user_agent(self, agent, platform, browser, device):
        response = requests.get("https://playground.learnqa.ru/ajax/api/user_agent_check",
                                headers={"User-Agent": agent})
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecoderError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"
        assert "platform" in response_as_dict, f"Response JSON doesn't have key 'platform'"
        assert "browser" in response_as_dict, f"Response JSON doesn't have key 'browser'"
        assert "device" in response_as_dict, f"Response JSON doesn't have key 'device'"
        detected_platform = response_as_dict["platform"]
        detected_browser = response_as_dict["browser"]
        detected_device = response_as_dict["device"]
        if detected_platform != platform:
            print(f"Platform of user-agent '{agent}' detected incorrectly, expected Platform is '{platform}'"
                  f" returned Platform is '{detected_platform}'")
        if detected_browser != browser:
            print(f"Browser  of user-agent '{agent}' detected incorrectly, expected Browser is '{browser}'"
                  f" returned Browser is '{detected_browser}'")
        if detected_device != device:
            print(f"Device of user-agent '{agent}' detected incorrectly, expected Device is '{device}'"
                  f" returned Device is '{detected_device}'")