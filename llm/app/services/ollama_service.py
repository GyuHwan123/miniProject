import ollama


class OllamaService:

    def summarize(self, text: str):

        prompt = f"""
다음 문서를 5줄 이내로 요약해줘.

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