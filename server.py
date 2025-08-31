
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os

from test import main, parse_structured_disease_info


app = FastAPI()

@app.post("/diagnose/")
async def diagnose_plant(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
        raise HTTPException(status_code=400, detail="Chỉ hỗ trợ ảnh JPG, PNG.")

    temp_path = f"temp_uploads/{file.filename}"
    os.makedirs("temp_uploads", exist_ok=True)
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        raw_text = main(temp_path)  # string: đầu ra từ LLM
        structured_result = parse_structured_disease_info(raw_text)
        return JSONResponse(content=structured_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        os.remove(temp_path)
