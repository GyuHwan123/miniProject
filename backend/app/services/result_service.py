from fastapi import HTTPException
from fastapi.responses import Response

class ResultService:
    # 1. OCR 결과만 가져오기
    @staticmethod
    async def get_ocr_result(task_id: str):
        # TODO: DB/Repository에서 OCR 텍스트 조회
        return {
            "task_id": task_id,
            "ocr_text": f"[{task_id}] 파일에서 추출된 OCR 텍스트입니다."
        }

    # 2. [LLM 요약하기] 버튼을 눌렀을 때 실행되는 요약 함수
    @staticmethod
    async def generate_llm_summary(task_id: str):
        # 1) OCR 텍스트를 먼저 가져옴
        ocr_data = await ResultService.get_ocr_result(task_id)
        ocr_text = ocr_data["ocr_text"]

        # 2) TODO: 팀원이 작성한 LLM 서비스(llm_service.py) 연동하기
        # summary_text = await llm_service.summarize(ocr_text)
        
        # 테스트용 결과
        summary_text = f"■ [{task_id}] 문서 요약 결과\n- 주요 내용이 성공적으로 요약되었습니다."

        return {
            "task_id": task_id,
            "llm_result": summary_text
        }

    # 3. 파일 다운로드 (OCR 또는 LLM 선택)
    @staticmethod
    async def download_file(task_id: str, file_type: str, content_text: str = ""):
        if file_type == "ocr":
            filename = f"{task_id}_ocr.txt"
        elif file_type == "llm":
            filename = f"{task_id}_summary.txt"
        else:
            raise HTTPException(status_code=400, detail="유효하지 않은 file_type입니다.")

        return Response(
            content=content_text.encode("utf-8"),
            media_type="text/plain; charset=utf-8",
            headers={"Content-Disposition": f"attachment; filename*=UTF-8''{filename}"}
        )