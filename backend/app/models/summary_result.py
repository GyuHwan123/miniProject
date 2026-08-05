from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class SummaryResult(Base):
    __tablename__ = "summary_result"

    summary_id = Column(Integer, primary_key=True, index=True)

    document_id = Column(
        Integer,
        ForeignKey("document.document_id"),
        nullable=False
    )

    summary_text = Column(Text, nullable=False)

    document = relationship(
        "Document",
        back_populates="summary_results"
    )