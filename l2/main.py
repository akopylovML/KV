import requests
import time

response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
token = response.json()["token"]
timeout = response.json()["seconds"]

response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params = {"token": token})
if response.json()["status"] != "Job is NOT ready":
    print("Job has wrong status")
time.sleep(timeout)
response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params = {"token": token})
if response.json()["status"] == "Job is ready" and "result" in response.json():
    print("Job is OK")
    print(response.json())
else:
    print("Job is broken")
    print(response.json())