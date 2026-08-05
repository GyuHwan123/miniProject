from urllib import response
from app.schemas.result import SummarizeRequest, SummarizeResponse
from app.services.result_service import ResultService
from app.schemas.summary_request import SummaryRequest
from app.schemas.summary_response import SummaryResponse
from app.services.summary_service import summary_service
from fastapi import APIRouter, HTTPException, UploadFile, File, Form

import requests


router = APIRouter()

@router.post("/api/summarize")
async def request_summarize(payload: SummarizeRequest):
    print(f"\n[1. LLM 요약 요청 수신] 입력 텍스트 길이: {len(payload.text)}자")
    print(f"[2. Gemma로 보낼 텍스트 일부]: {payload.text[:60]}...")
    
    try:
        # ⭕ payload.text (순수 텍스트 문자열)만 전달
        summary_result = summary_service.summarize(payload.text)
        
        print(f"[3. Gemma 요약 완료 결과]:\n{summary_result}\n")

        return {
            "status": "success",
            "task_id": payload.task_id,
            "llm_result": summary_result,
            "summary": summary_result
        }
    except Exception as e:
        print(f"❌ [Ollama 실행 실패]: {e}")
        return {
            "status": "error",
            "summary": f"요약 중 오류가 발생했습니다: {str(e)}"
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

@router.post("/api/ocr/upload")
async def upload(file: UploadFile = File(...),ocr_type: str = Form(...)):

    try:
        files = {
            "file": (
                file.filename,
                await file.read(),
                file.content_type,
            )
        }
    
        response = requests.post(
            "http://localhost:8002/api/ocr/upload",
            files=files,
            data={"ocr_type": ocr_type},
        )
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"OCR 서버 연결 실패: {str(e)}"
        )
    

    print("status =", response.status_code)
    print("text =", response.text)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )

    return response.json()


@router.post("/api/ocr/test")
async def ocr_test(
    file: UploadFile = File(...),
    ocr_type: str = Form(...)
):
    # 프론트엔드에서 날아온 파일명과 ocr_type 확인용 프린트
    print(f"[TEST] 받은 파일: {file.filename}, 선택한 OCR: {ocr_type}")
    
    # LLM(8001번)으로 바로 보낼 테스트용 더미 OCR 텍스트 반환
    return {
        "status": "success",
        "task_id": "test_task_123",
        "ocr_text": f"[테스트 OCR 결과 데이터]\n- 파일명: {file.filename}\n- 엔진: {ocr_type}\n- \n더미 데이터: 김\n해\n군\n우621\n010/경남\n김해시\n61\n-1/전화052530 -1351/전송1052536\n-1978담당배병급\n/\n문서번호\n지경\n55142\n둔\nY\n군\n수\n94 7 7\nY롱Y\n보존\nAyv\n경\n유\n[제1안]\n-\n-\n부\n군'\n수\n신\n장\n조\n겨\n장\n기안\n협조\n제\n목\n공장설립\n신고수리\n|하2\n장유면\n864번지\n주\n표\nY\n을\n으로\n부터\n공업배치및공장설립에관한법률\n13조\n제\n1항의\n규정에\n의거\n공장설립\n신고가\n108\n동법시행령\n2항의\n규정에\n의거\n제\n19조\n|0큰\n수리하고\n별첨\n공장설립\n신고\n를Y놓\n교부코자\n기거\n2\nI|이러군흐Y\n철저를\n기하고자\n이\n붕\n를ㄹ을\n-\n지정코자\n기거\n변경\n신고수리\n사항\n경\n-\n명[\n소재지\n대지면적m\n건축면적m?\n-\n-\n대\n'표'자\n송\n주서륭\n클프이어\n10655\n880162\n유하\n864번지외8필\n그직물제조업\n공장설립\nY뇨\n첨\n부\n신고\n1부\n조건사항\n1부\n2\n[제2안]\n수\n굶용요\n러음용\n864번지\n주\n신\n서륭\n표\n제3목\n공장설립\n신고수리\nㄱ울\n귀하께서\n공장설립\n신청하신\n변경\n신고에\n어왜\n공업배치\n및\n10클류요운\n제\n19조\n2항의\n규정에\n의거\n어로\n조건부\n수리하고\n공장설립\n변경\n15"
    }

