import requests
from fastapi import UploadFile

OCR_SERVER = "http://127.0.0.1:8002"

async def upload_ocr(file: UploadFile, model: str = "easy"):

    files = {
        "file": (
            file.filename,
            await file.read(),
            file.content_type
        )
    }

    response = requests.post(
        f"{OCR_SERVER}/api/ocr/upload",
        files=files,
        data={
            "ocr_type": model
        }
    )

    response.raise_for_status()

    return response.json()