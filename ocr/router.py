from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import Optional
from accuracy import parse_gt_file

router = APIRouter(
    prefix="/api/ocr",
    tags=["OCR"]
)


@router.post("/upload")
async def upload(
    file: UploadFile = File(...),
    ocr_type: str = Form(...),
    gt_file: Optional[UploadFile] = File(None),
):
    gt_text = await parse_gt_file(gt_file)

    if ocr_type == "easy":
        from eocr import process_easyocr
        return await process_easyocr(file, gt_text=gt_text)

    elif ocr_type == "paddle":
        from pocr import process_paddleocr
        return await process_paddleocr(file, gt_text=gt_text)

    else:
            return JSONResponse(
            status_code=400, 
            content={"message": "지원하지 않는 OCR 모델입니다."}
            )

    