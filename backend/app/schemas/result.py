from pydantic import BaseModel

# 요약 요청 스키마 (프론트가 보내주는 텍스트 받기)
class SummarizeRequest(BaseModel):
    task_id: str = "temp_id"
    text: str # 요약할 OCR 텍스트

# 요약 응답 스키마
class SummarizeResponse(BaseModel):
    task_id: str
    llm_result: str
    status: str = "success" ##DB없는경우