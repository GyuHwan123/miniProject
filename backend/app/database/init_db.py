from app.database.database import Base, engine

# 모델 import (매우 중요)
from app.models.document import Document
from app.models.ocr_result import OCRResult
from app.models.summary_result import SummaryResult

Base.metadata.create_all(bind=engine)

print("테이블 생성 완료!")