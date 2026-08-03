from pydantic import BaseModel

# 1. OCR 조회 응답 스키마
class OcrResultResponse(BaseModel):
    task_id: str
    ocr_text: str
    status: str = "success"

# 2. LLM 요약 실행 요청 스키마 (필요시 추가 옵션 전달 가능)
class SummaryRequest(BaseModel):
    task_id: str

# 3. LLM 요약 결과 응답 스키마
class SummaryResultResponse(BaseModel):
    task_id: str
    llm_result: str
    status: str = "success"