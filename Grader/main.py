import os
import tempfile

from fastapi import FastAPI, UploadFile, File, HTTPException
from utils.pdf_processor import pdf_processor
from utils.grader import grader

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/grade")
async def grade(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        questions, answers = pdf_processor(temp_file_path)
        grader_response = grader(questions[1], answers[1])

        return {"results": grader_response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if "temp_pdf_path" in locals() and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
