from fastapi import APIRouter, UploadFile, File, Form

router = APIRouter(
    prefix="/api/ocr",
    tags=["OCR"]
)


@router.post("/upload")
async def upload(
    file: UploadFile = File(...),
    ocr_type: str = Form(...),
):
    print("선택 OCR =", ocr_type)

    if ocr_type == "easy":
        from eocr import process_easyocr
        return await process_easyocr(file)

    elif ocr_type == "paddle":
        from pocr import process_paddleocr
        return await process_paddleocr(file)

    return {
        "message": "지원하지 않는 OCR 모델입니다."
    }