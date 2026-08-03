from app.services.ollama_service import ollama_service


class SummaryService:

    def summarize(self, text: str):

        return ollama_service.summarize(text)


summary_service = SummaryService()