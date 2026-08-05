from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class OCRResult(Base):
    __tablename__ = "ocr_result"

    ocr_id = Column(Integer, primary_key=True, index=True)

    document_id = Column(
        Integer,
        ForeignKey("document.document_id"),
        nullable=False
    )

    ocr_text = Column(Text, nullable=False)

    document = relationship(
        "Document",
        back_populates="ocr_results"
    )