import os
import xml.etree.ElementTree as ET
import requests
from fastapi import HTTPException
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
URL = "http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo"


def get_holidays(start_date, end_date):

    national_holidays = []
    for year in range(start_date.year, end_date.year + 1):
        params = {"serviceKey": SECRET_KEY, "solYear": year, "numOfRows": "30"}
        response = requests.get(URL, params=params)  # response type: xml

        # Raise an exception if API request fails
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"API request failed: {response.status_code}")

        # Parsing XML to get holiday date
        try:
            root = ET.fromstring(response.content)
            dates = [date.text for date in root.findall(".//locdate")]
            formatted_dates = [f"{date[:4]}년 {date[4:6]}월 {date[6:]}일" for date in dates]
            national_holidays.extend(formatted_dates)

        except ET.ParseError:
            raise HTTPException(status_code=500, detail="XML parsing error occurred")

    return national_holidays
