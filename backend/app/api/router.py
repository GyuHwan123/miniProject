from fastapi import APIRouter
from app.schemas.result import SummarizeRequest, SummarizeResponse
from app.schemas.summary_request import SummaryRequest
from app.schemas.summary_response import SummaryResponse
from app.services.result_service import ResultService
from app.services import summary_service

router = APIRouter()

@router.post("/api/summarize", response_model=SummarizeResponse)
async def request_summarize(payload: SummarizeRequest):
    # DB 조회 없이 프론트에서 넘어온 payload.text를 가지고 바로 LLM 요약 수행
    summary_text = await ResultService.generate_llm_summary(payload.text)
    
    return {
        "task_id": payload.task_id,
        "llm_result": summary_text
        }

@router.post("/llm/summary/test")
def test_summary():

    dummy_text = """
    인공지능은 다양한 산업에서 활용되고 있다.
    특히 OCR 기술과 LLM을 결합하면 문서를 자동으로 분석할 수 있다.
    사용자는 문서를 업로드하면 OCR을 통해 텍스트를 추출하고,
    이후 LLM이 내용을 요약하거나 분류한다.
    이러한 시스템은 업무 자동화에 큰 도움이 된다.
    """

    summary = summary_service.summarize(dummy_text)

    return {
        "ocr": dummy_text,
        "summary": summary
    }

@router.post("/llm/summary")
def summarize(req: SummaryRequest):

    summary = summary_service.summarize(req.text)

    return {
        "summary": summary

    }