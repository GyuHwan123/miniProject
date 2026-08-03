from fastapi import APIRouter
from app.schemas.result import SummarizeRequest, SummarizeResponse
from app.services.result_service import ResultService

router = APIRouter()

@router.post("/api/summarize", response_model=SummarizeResponse)
async def request_summarize(payload: SummarizeRequest):
    # DB 조회 없이 프론트에서 넘어온 payload.text를 가지고 바로 LLM 요약 수행
    summary_text = await ResultService.generate_llm_summary(payload.text)
    
    return {
        "task_id": payload.task_id,
        "llm_result": summary_text
    }