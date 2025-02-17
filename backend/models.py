from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class ExcelGenerationRequest(BaseModel):
    start_date: str = Field(strict=True)
    end_date: str = Field(strict=True)
    repeat_num: int = Field(strict=True, gt=0)

    # Check if the date format is YYYY-MM-DD and convert it to datetime.date
    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def validate_date_format(cls, value):
        try:
            value = datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError(f"Invalid date format: {value}. Use YYYY-MM-DD format.")

    # # Check if the repeat_count is a positive integer
    @field_validator("repeat_num", mode="before")
    @classmethod
    def validate_repeat_num(cls, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Repeat number must be greater than 0")
        return value

    # Check if the start_date is earlier than end_date
    @field_validator("end_date", mode="after")
    @classmethod
    def valid_date_order(cls, value, values):
        start_date = values.data.get("start_date")
        if start_date is None:
            raise ValueError("Start date is missing")

        end_date = value
        if start_date >= end_date:
            raise ValueError("Start date must be earlier than end date")

        return value
