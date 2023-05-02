import requests

response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(response.status_code)
print(response.text)

response = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method": "HEAD"})
print(response.status_code)
print(response.text)

response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method": "GET"})
print(response.status_code)
print(response.text)

methods = ["GET", "HEAD", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]

for method in methods:
    response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method": f"{method}"})
    # print(f"GET + {method} {response.status_code} {response.text}")
    if method == "GET" and response.text != '{"success":"!"}':
        print(f"Correct GET + {method} got failed response")
    elif method != "GET" and response.text == '{"success":"!"}':
        print(f"Wrong GET + {method} got correct response")
    response = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": f"{method}"})
    # print(f"HEAD + {method} {response.status_code} {response.text}")
    if response.text == '{"success":"!"}':
        print(f"Wrong HEAD + {method} got correct response")
    response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": f"{method}"})
    # print(f"POST + {method} {response.status_code} {response.text}")
    if method == "POST" and response.text != '{"success":"!"}':
        print(f"Correct POST + {method} got failed response")
    elif method != "POST" and response.text == '{"success":"!"}':
        print(f"Wrong POST + {method} got correct response")
    response = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": f"{method}"})
    # print(f"PUT + {method} {response.status_code} {response.text}")
    if method == "PUT" and response.text != '{"success":"!"}':
        print(f"Correct PUT + {method} got failed response")
    elif method != "PUT" and response.text == '{"success":"!"}':
        print(f"Wrong PUT + {method} got correct response")
    response = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": f"{method}"})
    # print(f"DELETE + {method} {response.status_code} {response.text}")
    if method == "DELETE" and response.text != '{"success":"!"}':
        print(f"Correct DELETE + {method} got failed response")
    elif method != "DELETE" and response.text == '{"success":"!"}':
        print(f"Wrong DELETE + {method} got correct response")
    response = requests.options("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": f"{method}"})
    # print(f"OPTIONS + {method} {response.status_code} {response.text}")
    if response.text == '{"success":"!"}':
        print(f"Wrong OPTIONS + {method} got correct response")
    response = requests.patch("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": f"{method}"})
    # print(f"PATCH + {method} {response.status_code} {response.text}")
    if response.text == '{"success":"!"}':
        print(f"Wrong PATCH + {method} got correct response")