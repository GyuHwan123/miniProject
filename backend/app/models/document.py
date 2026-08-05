from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base


class Document(Base):
    __tablename__ = "document"

    document_id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255), nullable=False)

    ocr_results = relationship(
        "OCRResult",
        back_populates="document",
        cascade="all, delete-orphan"
    )

    summary_results = relationship(
        "SummaryResult",
        back_populates="document",
        cascade="all, delete-orphan"
    )