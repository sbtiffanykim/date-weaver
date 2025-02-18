import requests
import os
import xml.etree.ElementTree as ET
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

url = "http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo"
params = {"serviceKey": SECRET_KEY, "solYear": "2025", "numOfRows": "30"}

response = requests.get(url, params=params)  # response type: xml
root = ET.fromstring(response.content)

national_holidays = []

for day in root.iter("locdate"):
    national_holidays.append(day.text)

# print(national_holidays)
# print(len(national_holidays))
