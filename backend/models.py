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
