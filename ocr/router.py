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
    gt_file: Optional[UploadFile] = File(None),
    model: str = Form("easy"),    
):
    gt_text = await parse_gt_file(gt_file)

    
    if model == "easy":
        # 필요한 순간에만 EasyOCR import
        from eocr import process_easyocr
        return await process_easyocr(file, gt_text=gt_text)

    elif model == "paddle":
        # 필요한 순간에만 PaddleOCR import
        from pocr import process_paddleocr
        return await process_paddleocr(file, gt_text=gt_text)

    else:
        return JSONResponse(
        status_code=400, 
        content={"message": "지원하지 않는 OCR 모델입니다."}
        )
       
    
