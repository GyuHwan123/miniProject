import os
import io
from typing import Optional
import time
from fastapi import UploadFile
from fastapi.responses import JSONResponse
import easyocr
from pdf2image import convert_from_bytes
from docx import Document
import win32com.client
import tempfile

MAX_FILE_SIZE = 20 * 1024 * 1024
reader = easyocr.Reader(['ko', 'en'], gpu=False) 

from quality import calculate_text_quality_score
from accuracy import calculate_cer_accuracy

def parse_txt(file_bytes: bytes) -> tuple[str, float]:
    """TXT 바이너리에서 인코딩 자동 감지 후 텍스트 및 정확도 추출"""
    extracted_text = ""
    # 1. UTF-8 시도
    try:
        extracted_text = file_bytes.decode('utf-8')
    except UnicodeDecodeError:
        # 2. CP949 (한글 Windows 기본) 시도
        try:
            extracted_text = file_bytes.decode('cp949')
        except UnicodeDecodeError:
            extracted_text = file_bytes.decode('utf-8', errors='ignore')

    score = calculate_text_quality_score(extracted_text)
    return extracted_text.strip(), score

def parse_docx(file_bytes: bytes) -> str:
    """DOCX 바이너리 데이터에서 텍스트를 추출합니다."""
    doc = Document(io.BytesIO(file_bytes))
    full_text = [para.text for para in doc.paragraphs if para.text.strip()]
    extracted_text = "\n".join(full_text)
    score = calculate_text_quality_score(extracted_text)
    return extracted_text, score

def parse_hwp(file_bytes: bytes) -> str:
    """HWP 문서를 TXT 파일로 바로 덤프하여 매개변수 및 클립보드 오류 해결"""
    hwp_temp_path = None
    txt_temp_path = None
    hwp_app = None
    extracted_text = ""
    
    try:
        # 1. 임시 HWP 파일 생성 및 락 해제
        with tempfile.NamedTemporaryFile(delete=False, suffix=".hwp") as tmp:
            tmp.write(file_bytes)
            hwp_temp_path = tmp.name

        txt_temp_path = hwp_temp_path.replace(".hwp", ".txt")

        # 2. 한글 COM 객체 생성
        hwp_app = win32com.client.Dispatch("HWPFrame.HwpObject")
        
        # 3. 보안 승인 모듈 등록 (보안 팝업으로 인한 엉뚱한 텍스트 추출 방지)
        # 보안 모듈이 없어도 구동되도록 예외 처리
        try:
            hwp_app.RegisterModule("FilePathCheckDLL", "FilePathCheckRegister")
        except Exception:
            pass

        # 4. 문서 열기 (인자 3개 명시)
        hwp_app.Open(hwp_temp_path, "HWP", "")
        
        # 5. 텍스트 파일(TEXT 포맷)로 직접 저장 (매개변수 3개 확실히 전달)
        # "TEXT" 포맷 키워드를 전달하면 본문 텍스트만 .txt 파일로 내보냅니다.
        hwp_app.SaveAs(txt_temp_path, "TEXT", "")
        
        # 6. 한글 프로세스 종료
        hwp_app.Quit()
        hwp_app = None

        # 7. 생성된 TXT 파일을 파이썬이 읽기 (CP949 또는 UTF-8)
        if os.path.exists(txt_temp_path):
            # 한글 텍스트 저장 기본 인코딩은 보통 cp949/euc-kr
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
        return f"HWP 파싱 에러: {str(e)}", 0.0
        
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

def process_local_ocr(file_bytes: bytes, extension: str) -> str:
    """다양한 문서 포맷(이미지, PDF, TXT, DOCX, HWP)에서 로컬 텍스트를 추출합니다."""
    try:
        # 1. 텍스트 파일 (.txt)
        if extension == "txt":
            return parse_txt(file_bytes)

        # 2. 워드 파일 (.docx)
        elif extension == "docx":
            return parse_docx(file_bytes)

        # 3. 한글 파일 (.hwp)
        elif extension == "hwp":
            return parse_hwp(file_bytes)

        # 4. 다중 페이지 PDF 파일
        elif extension == "pdf":
            # poppler 에러가 난다면 poppler_path에 poppler의 bin 폴더가 있는 r"C:\실제경로" 를 명시
            images = convert_from_bytes(file_bytes, poppler_path=r"C:\Release-26.02.0-0\poppler-26.02.0\Library\bin") 
            if not images:
                return "PDF 파일에서 이미지를 추출할 수 없습니다.", 0.0
            
            full_text_list = []
            all_confidences = []

            for i, pil_image in enumerate(images):
                img_byte_arr = io.BytesIO()
                pil_image.save(img_byte_arr, format='PNG')
                ocr_input = img_byte_arr.getvalue()
                results = reader.readtext(ocr_input, detail=1)
                
                page_texts = []
                for _, text, prob in results:
                    page_texts.append(text)
                    all_confidences.append(prob)
                
                page_text = " ".join(page_texts)
                full_text_list.append(f"[Page {i+1}] {page_text}")
                
            avg_confidence = (sum(all_confidences) / len(all_confidences)) if all_confidences else 0.0
            return "\n".join(full_text_list), round(avg_confidence, 4)

        # 5. 일반 이미지 파일 (.jpg, .jpeg, .png)
        else:
            results = reader.readtext(file_bytes, detail=1)
            
            texts = []
            confidences = []
            for _, text, prob in results:
                texts.append(text)
                confidences.append(prob)
                
            avg_confidence = (sum(confidences) / len(confidences)) if confidences else 0.0
            return "\n".join(texts), round(avg_confidence, 4)
        
    except Exception as e:
        return f"텍스트 추출 중 오류 발생: {str(e)}"

async def process_easyocr(file: UploadFile, gt_text: Optional[str] = None):
    """파일(이미지/PDF/TXT/DOCX/HWP)을 업로드 받아 텍스트를 추출하는 엔드포인트"""
    # 실행 전 시간 측정
    request_start_time = time.perf_counter()

    # 0. 파일 용량 사전 검증 (20MB 초과 시 읽기 작업 전에 즉시 차단)
    file_size = getattr(file, "size", None)

    # size 속성을 직접 가져올 수 없는 경우 포인터 이동으로 측정
    if file_size is None:
        file.file.seek(0, 2)  # 파일 맨 끝으로 이동
        file_size = file.file.tell()  # 용량 측정
        file.file.seek(0)  # 커서를 다시 맨 앞으로 복구 (필수!)

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
    
    # 1. 파일 확장자 검증 (pdf, txt 포함)
    allowed_extensions = ["jpg", "jpeg", "png", "pdf", "txt", "docx", "hwp"]
    ext = file.filename.split(".")[-1].lower()
    if ext not in allowed_extensions:
        return JSONResponse(
            status_code=400, 
            content={"message": f"지원하지 않는 파일 형식입니다. ({', '.join(allowed_extensions)}만 가능)"}
        )
    
    # 2. 파일 읽기
    file_bytes = await file.read()    
    # 3. 확장자별 처리 및 텍스트 추출
    parsing_start_time = time.perf_counter()
    parsed_text, default_score = process_local_ocr(file_bytes, ext)

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

    # 파싱 소요 시간 (초 단위, 소수점 3자리 반올림)
    parsing_duration = round(parsing_end_time - parsing_start_time, 3)
    # 4. 전체 요청 처리 소요 시간 측정
    request_end_time = time.perf_counter()
    total_duration = round(request_end_time - request_start_time, 3)
    
    # 5. 결과 반환
    return {
        "filename": file.filename,
        "ocr_text": parsed_text,
        "model_used": "EasyOCR",
        "accuracy_info": acc_info,
        "parsing_time_seconds": parsing_duration,
        "total_api_time_seconds": total_duration
    }

