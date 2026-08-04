import os
import io
import time
import tempfile
import win32com.client
from fastapi import FastAPI, UploadFile, File, status
from fastapi.responses import JSONResponse
from pdf2image import convert_from_bytes
from PIL import Image
import numpy as np
from paddleocr import PaddleOCR
import fitz

app = FastAPI()

# -------------------------------------------------------------
# PaddleOCR 전역 객체 초기화 (서버 시작 시 1회 로드)
# lang='korean'으로 지정하여 한국어/영어 동시 지원
# use_gpu=False (기본 CPU 동작. GPU 사용 환경이라면 True로 변경)
# -------------------------------------------------------------
ocr_engine = PaddleOCR(use_angle_cls=True, lang='korean', use_gpu=False)

# 파일 용량 제한 (20MB)
MAX_FILE_SIZE = 20 * 1024 * 1024  
# poppler가 설치된 bin 폴더 경로를 지정해 줍니다.
POPPLER_PATH = r"C:\Release-26.02.0-0\poppler-26.02.0\Library\bin"

def parse_image_with_paddle(file_bytes: bytes) -> str:
    """PaddleOCR을 이용한 이미지 텍스트 추출 함수"""
    extracted_lines = []
     
        # 1. 이미지 처리
    image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    img_np = np.array(image) # PaddleOCR은 Numpy Array 입력을 받습니다.
        
        # PaddleOCR 수행
    result = ocr_engine.ocr(img_np, cls=True)
        
        # 결과 처리 (result -> [page_result -> [ [[box], (text, score)], ... ]])
    if result and result[0]:
        for line in result[0]:
            text = line[1][0]  # (텍스트, 신뢰도) 중 텍스트 선택
            extracted_lines.append(text)
            
    return "\n".join(extracted_lines)

def parse_pdf_with_paddle(file_bytes: bytes) -> str:
    """Poppler 설치 없이 파이썬 라이브러리로만 PDF를 OCR하는 함수"""
    extracted_lines = []
    
    # 메모리의 PDF 바이트 데이터를 읽기
    pdf_doc = fitz.open(stream=file_bytes, filetype="pdf")
    
    for page_idx, page in enumerate(pdf_doc):
        # PDF 페이지를 고해상도 이미지(PixMap)로 렌더링 (DPI 200 수준 설정)
        pix = page.get_pixmap(dpi=150)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img_np = np.array(img)
        
        # PaddleOCR 수행
        result = ocr_engine.ocr(img_np, cls=True)
        
        page_text = []
        if result and result[0]:
            for line in result[0]:
                page_text.append(line[1][0])
                
        extracted_lines.append(f"--- [Page {page_idx + 1}] ---")
        extracted_lines.append("\n".join(page_text))
        
    return "\n".join(extracted_lines)

def parse_hwp(file_bytes: bytes) -> str:
    """HWP 텍스트(TEXT) 덤프 추출 (기존 COM 코드 유지)"""
    hwp_temp_path = None
    txt_temp_path = None
    hwp_app = None
    
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
                    return f.read().strip()
            except UnicodeDecodeError:
                with open(txt_temp_path, "r", encoding="utf-8", errors="ignore") as f:
                    return f.read().strip()
        return "HWP 변환 실패"
    except Exception as e:
        return f"HWP 오류: {str(e)}"
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


def process_local_ocr(file_bytes: bytes, ext: str) -> str:
    """확장자별 문서 파싱 분기"""
    if ext in ["jpg", "jpeg", "png"]:
        return parse_image_with_paddle(file_bytes)
    elif ext == "pdf":
        return parse_pdf_with_paddle(file_bytes)
    elif ext == "hwp":
        return parse_hwp(file_bytes)
    elif ext == "txt":
        try:
            return file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            return file_bytes.decode("cp949", errors="ignore")
    elif ext == "docx":
        import docx
        doc = docx.Document(io.BytesIO(file_bytes))
        return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    return "지원하지 않는 형식을 우회함"


@app.post("/upload-ocr/")
async def upload_and_process_ocr(file: UploadFile = File(...)):
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
    parsed_text = process_local_ocr(file_bytes, ext)
    parsing_end_time = time.perf_counter()

    parsing_duration = round(parsing_end_time - parsing_start_time, 3)

    # 4. 전체 요청 처리 소요 시간 측정
    request_end_time = time.perf_counter()
    total_duration = round(request_end_time - request_start_time, 3)
    
    # 5. 결과 반환
    return {
        "filename": file.filename,
        "extracted_text": parsed_text,
        "model_used": "PaddleOCR + Native Document Parsers",
        "parsing_time_seconds": parsing_duration,
        "total_api_time_seconds": total_duration
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("pocr:app", host="127.0.0.1", port=8000, reload=True)