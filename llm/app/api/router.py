from fastapi import APIRouter
from app.schemas.summary_request import SummaryRequest
from app.schemas.summary_response import SummaryResponse
from app.services.summary_service import summary_service

router = APIRouter()

@router.post("/llm/summary")
def summarize(req: SummaryRequest):

    summary = summary_service.summarize(req.text)

    return {
        "summary": summary
    }