import os
import io
import time
import tempfile
from docx import Document
import win32com.client
from fastapi import UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import numpy as np
from pdf2image import convert_from_bytes
from typing import Optional
import gc
import torch
import cv2

# 파일 용량 제한 (20MB)
MAX_FILE_SIZE = 20 * 1024 * 1024  

from quality import calculate_text_quality_score
from accuracy import calculate_cer_accuracy
from model_manager import get_ocr_engine

ocr_engine = get_ocr_engine("paddleocr")

def parse_image_with_paddle(file_bytes: bytes) -> str:
    """PaddleOCR을 이용한 이미지 텍스트 추출 함수"""

    result = ocr_engine.ocr(file_bytes, cls=True)

    texts = []
    confidences = []

    if result:
        # PaddleOCR의 리스트 중첩(Depth) 변동 완벽 방어
        lines = result[0] if (isinstance(result, list) and len(result) > 0 and result[0] is not None) else []

        for line in lines:
            if not line or len(line) < 2:
                continue
            
            text_info = line[1] # ("텍스트", 점수)
            if isinstance(text_info, (tuple, list)) and len(text_info) >= 2:
                text = text_info[0]
                score = float(text_info[1])
                
                # 유효 점수만 수집
                texts.append(text)
                confidences.append(score)

    # 2. 정확한 산술 평균 계산
    if confidences:
        avg_confidence = sum(confidences) / len(confidences)
    else:
        avg_confidence = 0.0

    return "\n".join(texts), round(avg_confidence, 4)
    

def parse_pdf_with_paddle(file_bytes: bytes) -> str:
    images = convert_from_bytes(
        file_bytes, 
        poppler_path=r"C:\Release-26.02.0-0\poppler-26.02.0\Library\bin"
    )
    if not images:
        return "PDF 파일에서 이미지를 추출할 수 없습니다.", 0.0

    full_text_list = []
    all_confidences = []

    for i, pil_image in enumerate(images):       
        img_np = np.ascontiguousarray(np.array(pil_image.convert("RGB"), dtype=np.uint8))
        img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        result = ocr_engine.ocr(img_bgr, cls=True)

        page_texts = []
        if result and result[0]:
            for line in result[0]:
                # line 구조: [ [[x1,y1],...], ("텍스트", 신뢰도) ]
                text = line[1][0]
                prob = line[1][1] # float 형태의 정확한 신뢰도 점수
                
                page_texts.append(text)
                all_confidences.append(prob)

        page_text = " ".join(page_texts)
        full_text_list.append(f"[Page {i+1}] {page_text}")

    avg_confidence = (sum(all_confidences) / len(all_confidences)) if all_confidences else 0.0
    del images

    return "\n".join(full_text_list), round(avg_confidence, 4)

def parse_txt(file_bytes: bytes) -> tuple[str, float]:
    """TXT 파일 파싱 및 유효성 점수 계산"""
    try:
        text = file_bytes.decode("utf-8")
    except UnicodeDecodeError:
        text = file_bytes.decode("cp949", errors="ignore")
    
    text = text.strip()
    score = calculate_text_quality_score(text)
    return text, score

def parse_docx(file_bytes: bytes) -> tuple[str, float]:
    """DOCX 파일 파싱 및 유효성 점수 계산"""
    doc = Document(io.BytesIO(file_bytes))
    full_text = [p.text for p in doc.paragraphs if p.text.strip()]
    text = "\n".join(full_text)
    score = calculate_text_quality_score(text)
    return text, score

def parse_hwp(file_bytes: bytes) -> str:
    """HWP 텍스트(TEXT) 덤프 추출 (기존 COM 코드 유지)"""
    hwp_temp_path = None
    txt_temp_path = None
    hwp_app = None
    extracted_text = ""
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".hwp") as tmp:
            tmp.write(file_bytes)
            hwp_temp_path = tmp.name

        txt_temp_path = hwp_temp_path.replace(".hwp", ".txt")
        hwp_app = win32com.client.Dispatch("HWPFrame.HwpObject")
        
        try:
            hwp_app.RegisterModule("FilePathCheckDLL", "FilePathCheckRegister")
        except Exception:
            pass

        hwp_app.Open(hwp_temp_path, "HWP", "")
        hwp_app.SaveAs(txt_temp_path, "TEXT", "")
        hwp_app.Quit()
        hwp_app = None

        if os.path.exists(txt_temp_path):
            try:
                with open(txt_temp_path, "r", encoding="cp949") as f:
                    extracted_text = f.read()
            except UnicodeDecodeError:
                with open(txt_temp_path, "r", encoding="utf-8", errors="ignore") as f:
                    extracted_text = f.read()

            extracted_text = extracted_text.strip()
            score = calculate_text_quality_score(extracted_text)
            return extracted_text, score
        else:
            return "HWP 텍스트 파일 변환 실패", 0.0

        
    except Exception as e:
        return f"HWP 오류: {str(e)}", 0.0
    finally:
        if hwp_app is not None:
            try: hwp_app.Quit()
            except: pass
        if hwp_temp_path and os.path.exists(hwp_temp_path):
            try: os.remove(hwp_temp_path)
            except: pass
        if txt_temp_path and os.path.exists(txt_temp_path):
            try: os.remove(txt_temp_path)
            except: pass


def process_local_ocr(file_bytes: bytes, ext: str) -> tuple[str, float]:
    """확장자별 문서 파싱 분기"""
    ocr_engine = get_ocr_engine("paddleocr")
    try:
        if ext in ["jpg", "jpeg", "png"]:
            return parse_image_with_paddle(file_bytes)
        elif ext == "pdf":
            return parse_pdf_with_paddle(file_bytes)
        elif ext == "hwp":
            return parse_hwp(file_bytes)
        elif ext == "txt":
            return parse_txt(file_bytes)
        elif ext == "docx":
            return parse_docx(file_bytes)
        return "지원하지 않는 형식을 우회함", 0.0
    except Exception as e:
        return f"텍스트 추출 중 오류 발생: {str(e)}", 0.0


async def process_paddleocr(file: UploadFile, gt_text: Optional[str] = None):
    """파일(이미지/PDF/TXT/DOCX/HWP) 업로드 및 텍스트 추출 라우터"""

    # 전체 요청 시작 시간 측정
    request_start_time = time.perf_counter()

    # 0. 파일 용량 사전 검증 (20MB)
    file_size = getattr(file, "size", None)
    if file_size is None:
        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)

    if file_size > MAX_FILE_SIZE:
        max_mb = MAX_FILE_SIZE / (1024 * 1024)
        current_mb = file_size / (1024 * 1024)
        return JSONResponse(
            status_code=413,
            content={
                "message": f"파일 크기가 제한({max_mb:.0f}MB)을 초과했습니다.",
                "current_size": f"{current_mb:.2f}MB"
            }
        )

    # 1. 파일 확장자 검증
    allowed_extensions = ["jpg", "jpeg", "png", "pdf", "txt", "docx", "hwp"]
    ext = file.filename.split(".")[-1].lower()
    if ext not in allowed_extensions:
        return JSONResponse(
            status_code=400, 
            content={"message": f"지원하지 않는 파일 형식입니다. ({', '.join(allowed_extensions)}만 가능)"}
        )
    
    # 2. 파일 데이터 읽기
    file_bytes = await file.read()
    
    # 3. 텍스트 추출 실행
    parsing_start_time = time.perf_counter()
    try:
            parsed_text, default_score = process_local_ocr(file_bytes, ext)
    
    except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    finally:
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

    # Ground Truth가 들어온 경우: 원문 대조 정확도 계산
    if gt_text and gt_text.strip():
        acc_info = calculate_cer_accuracy(gt_text=gt_text, pred_text=parsed_text)
        acc_info["evaluation_type"] = "Ground Truth Comparison (CER)"
    # Ground Truth가 없는 경우: 기존 모델 신뢰도 / 유효성 점수 유지
    else:
        acc_info = {
            "score": default_score,
            "accuracy_percentage": f"{round(default_score * 100, 2)}%",
            "evaluation_type": "Model Confidence / Text Validity"
        }
        
    parsing_end_time = time.perf_counter()

    parsing_duration = round(parsing_end_time - parsing_start_time, 3)

    # 4. 전체 요청 처리 소요 시간 측정
    request_end_time = time.perf_counter()
    total_duration = round(request_end_time - request_start_time, 3)
    
    # 5. 결과 반환
    return {
        "filename": file.filename,
        "ocr_text": parsed_text,
        "model_used": "PaddleOCR + Native Document Parsers",
        "accuracy_info": acc_info,
        "parsing_time_seconds": parsing_duration,
        "total_api_time_seconds": total_duration
    }

