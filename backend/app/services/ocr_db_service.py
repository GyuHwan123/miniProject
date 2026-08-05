from sqlalchemy.orm import Session
from app.models.ocr_result import OCRResult


class OCRDBService:

    @staticmethod
    def save(
        db: Session,
        filename: str,
        ocr_text: str
    ):

        data = OCRResult(
            filename=filename,
            content=ocr_text
        )

        db.add(data)
        db.commit()
        db.refresh(data)

        return data