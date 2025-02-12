from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from excel_utils import generate_excel


class ExcelGenerationRequest(BaseModel):
    start_date: str
    end_date: str
    repeat_num: int


app = FastAPI()


@app.post("/generate-file")
async def create_file(data: ExcelGenerationRequest):
    try:
        file_path = generate_excel(data.start_date, data.end_date, data.repeat_num)
        return FileResponse(
            file_path,
            filename="generated_dates.xlsx",
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            status_code=200,
        )
    except HTTPException as e:
        return {"error": e.detail}
