import ollama


class OllamaService:

    def summarize(self, text: str):

        prompt = f"""
        당신은 OCR로 추출된 불완전한 문서를 정제하고 요약하는 전문 문서 분석가입니다.
        제공된 OCR 텍스트를 분석하여 아래 [출력 양식]에 맞추어 깔끔하게 정리해 주세요.

        [처리 지침]
        1. 문서의 주제와 내용에 맞는 가장 적절한 '카테고리'를 1개 지정하세요. (예: 문서/보고서, 영수증/청구서, 계약서, 공지사항, 매뉴얼, 기타)
        2. OCR 오타나 부자연스러운 띄어쓰기를 자연스럽게 교정하세요.
        3. 문서의 전체 내용을 단락별로 구분하고, 표(Table)나 목록(List) 형태가 포함되어 있다면 마크다운(Markdown) 표/기호로 보기 좋게 복원하세요.
        4. 단순히 줄 수만 줄이는 요약이 아니라, 문서의 **핵심 정보를 보존하면서 가독성 높게 전체 구조화**를 진행하세요.
        5. 오직 정리된 결과만 출력하고, 서론/인삿말/부연 설명은 절대 출력하지 마세요.

        [출력 양식]
        ■ 카테고리: [분류된 카테고리명]

        ■ 핵심 요약
        - [문서의 핵심 목적이나 요점 1~3줄]

        ■ 상세 내용
        [문서의 전체 내용을 구조화된 마크다운 텍스트, 목록(-, 1.), 마크다운 표(|) 등을 활용하여 보기 좋게 작성]

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

        return response["message"]["content"]


ollama_service = OllamaService()