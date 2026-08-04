import requests


class SummaryService:

    def summarize(self, text: str):

        response = requests.post(
            "http://localhost:8001/llm/summary",
            json={
                "text": text
            }
        )

        return response.json()["summary"]


summary_service = SummaryService()