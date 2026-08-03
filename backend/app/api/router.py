from app.schemas.summary_request import SummaryRequest
from app.schemas.summary_response import SummaryResponse
from app.services import summary_service
from fastapi import APIRouter

router = APIRouter()


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