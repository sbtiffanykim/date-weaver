import datetime
import os
from openpyxl import Workbook
from openpyxl.styles import PatternFill
from fastapi import HTTPException


# Define national holidays
national_holidays = [
    "01월 01일",
    "03월 01일",
    "05월 05일",
    "05월 15일",
    "06월 06일",
    "08월 15일",
    "10월 03일",
    "10월 09일",
    "12월 25일",
]


# Convert weekday index to Korean name
def convert_day(day):
    days = ["월", "화", "수", "목", "금", "토", "일"]
    return days[day]


def generate_excel(start_date: str, end_date: str, repeat_num: int):

    start = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    end = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

    # Validate that start_date is before end_date
    if start > end:
        raise HTTPException(status_code=400, detail="Start date must be before end date.")

    difference = (end - start).days
    file = Workbook()

    # Create list of dates from start_date to end_date
    datelist = []
    for i in range(difference + 1):
        date = start + datetime.timedelta(days=i)
        day = convert_day(date.weekday())
        formatted_date = date.strftime("20%y년 %m월 %d일") + f"({day})"
        datelist.append(formatted_date)

    # Create worksheets based on repeat_num
    for n in range(1, repeat_num + 1):
        sheet = file.create_sheet(f"{n}개")
        sheet.column_dimensions["A"].width = 20

        all_dates = [date for date in datelist for _ in range(n)]

        # Populate sheet with dates
        for idx, item in enumerate(all_dates, start=1):
            sheet.append([item])  # Add date to Excel

            cell = sheet[f"A{idx}"]

            # Highlight Saturdays in red
            if "토" in item:
                cell.fill = PatternFill(start_color="ffcccc", end_color="ffcccc", fill_type="solid")

            # Highlight national holidays in orange
            if any(holiday in item for holiday in national_holidays):
                cell.fill = PatternFill(start_color="f5c77e", end_color="f5c77e", fill_type="solid")

    # Define the save directory
    save_dir = "temp_file"
    os.makedirs(save_dir, exist_ok=True)  # Create directory if it doesn't exist

    # Save the file
    filename = f"{start.month}월 - {end.month}월.xlsx"
    full_path = os.path.join(save_dir, filename)

    file.save(full_path)
    file.close()

    return full_path  # Return the path
