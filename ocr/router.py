import cv2
import os
import io
import tempfile
import shutil
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import Optional
from accuracy import parse_gt_file

from preprocess import preprocess_image

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
    gt_text = await parse_gt_file(gt_file) if gt_file else None #파일업로드 안됐을때 500뜨지않게 안전장치 추가
    ext = file.filename.split(".")[-1].lower() #파일 확장자 확인

    if ext in ["jpg", "jpeg", "png"]:
        # 원본 파일을 임시 저장 (preprocess_image가 파일 경로를 받기 때문)
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name
            
        try:
            processed_img = preprocess_image(tmp_path) #전처리 실행
            success, encoded_img = cv2.imencode(f".{ext}", processed_img)# 전처리된 이미지를 다시 바이트(Bytes)로 인코딩
            if success:
                processed_bytes = encoded_img.tobytes()
                
                file.file = io.BytesIO(processed_bytes)# FastAPI UploadFile 내부의 파일 스트림을 '전처리된 바이트'로 바꿔치기!
                file.file.seek(0) # 파일 읽기 커서 초기화
                
        finally:
            # 다 쓴 임시 원본 파일 삭제
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

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

    