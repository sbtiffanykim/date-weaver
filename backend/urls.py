import requests
import os
import xml.etree.ElementTree as ET
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

url = "http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo"


def get_holidays(start_date, end_date):

    years = [start_date.year]
    # if start_date year != end_date year
    if start_date.year != end_date.year:
        years.append(end_date.year)

    print(years)

    national_holidays = []
    for year in years:
        params = {"serviceKey": SECRET_KEY, "solYear": year, "numOfRows": "30"}
        response = requests.get(url, params=params)  # response type: xml
        # Parsing XML to get holiday date
        root = ET.fromstring(response.content)
        for day in root.iter("locdate"):
            date = day.text
            formatted_date = datetime.strptime(date, "%Y%m%d").strftime("%Y년 %m월 %d일")
            national_holidays.append(formatted_date)

    return national_holidays
