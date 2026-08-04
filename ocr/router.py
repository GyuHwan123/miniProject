from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/api/ocr",
    tags=["OCR"]
)


@router.post("/upload")
async def upload(
    file: UploadFile = File(...),
    model: str = Form("easy"),
):

    if model == "easy":
        # 필요한 순간에만 EasyOCR import
        from eocr import process_easyocr
        return await process_easyocr(file)

    elif model == "paddle":
        # 필요한 순간에만 PaddleOCR import
        from pocr import process_paddleocr
        return await process_paddleocr(file)

    return JSONResponse(
            status_code=400, 
            content={"message": "지원하지 않는 OCR 모델입니다."}
        )