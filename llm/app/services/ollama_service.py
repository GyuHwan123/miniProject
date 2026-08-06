import ollama


class OllamaService:

    def summarize(self, text: str):

        prompt = f"""
        당신은 OCR로 추출된 불완전한 문서를 정제하고 요약하는 전문 문서 분석가입니다.
        제공된 OCR 텍스트의 문맥과 사실관계(Fact)를 정확히 파악하여 오타를 교정하고, 아래 [출력 양식]에 맞추어 구조화해 주세요.

        [처리 지침]
        1. 사실 왜곡 엄금(매우 중요): OCR 텍스트에 기재된 사실(동의율 달성 여부, 날짜, 기관명, 진행 상황 등)을 절대 반대로 해석하거나 지어내지 마세요. 있는 사실 그대로만 작성하세요.
        2. 핵심 요약: 문서의 발송 목적과 현재 상황, 향후 계획을 3줄 이내의 개조식(Bullet point)으로 명확하게 요약하세요.
        3. 내용 정제: '동의울 80파클' -> '동의율 80%를'처럼 심한 OCR 오타와 부자연스러운 띄어쓰기를 문맥에 맞게 완벽히 교정하세요.
        4. 상세 내용 구조화: 서론-본론-결론 또는 시간 흐름에 따라 단락을 나누고, 마크다운(##, -, 1.)을 활용하여 가독성 있게 정리하세요.
        5. 카테고리 분류: 문서 성격에 맞는 카테고리 1개를 지정하세요. (예: 공지사항, 안내문, 공문, 계약서 등)
        6. 출력 제한: 인사말이나 부연 설명 없이, 오직 [출력 양식]에 해당하는 내용만 출력하세요.

        [출력 양식]
        ■ 카테고리: [분류된 카테고리명]

        ■ 핵심 요약
        - [문서의 핵심 목적이나 요점 1]
        - [요점 2]
        - [요점 3]

        ■ 상세 내용
        [문서를 자연스러운 문장으로 교정 및 마크다운 구조화]

        [OCR 텍스트]
        {text}
        """

        response = ollama.chat(
            model="gemma3:1b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        # 💡 [핵심 수정 위치] 
        # 대괄호 ['message']['content'] 대신 점(.) 속성 접근 방식을 사용합니다.
        try:
            # Pydantic 객체 속성 접근
            return response.message.content
        except AttributeError:
            # 만약 구버전 딕셔너리로 들어올 경우 예외 처리
            return response['message']['content']


ollama_service = OllamaService()