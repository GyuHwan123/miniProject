from fastapi import APIRouter, Query
from app.schemas.result import OcrResultResponse, SummaryRequest, SummaryResultResponse
from app.services.result_service import ResultService

router = APIRouter()

# 1. 페이지 진입 시: OCR 결과 조회
@router.get("/results/{task_id}/ocr", response_model=OcrResultResponse)
async def get_ocr_result(task_id: str):
    return await ResultService.get_ocr_result(task_id)


# 2. [LLM 요약하기] 버튼 클릭 시: 요약 생성 및 결과 반환
@router.post("/results/summarize", response_model=SummaryResultResponse)
async def request_llm_summary(payload: SummaryRequest):
    return await ResultService.generate_llm_summary(payload.task_id)


# 3. 결과 다운로드 API
@router.get("/download/{task_id}")
async def download_result(
    task_id: str, 
    type: str = Query(..., description="'ocr' 또는 'llm'")
):
    # 실제로는 DB에서 가져오거나 프론트에서 받은 텍스트로 다운로드 생성
    sample_text = "다운로드할 텍스트 내용입니다."
    return await ResultService.download_file(task_id, type, sample_text)