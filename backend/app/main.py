from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import router as api_router

app = FastAPI(title="OCR & LLM Project")

# ⭕ 만드신 라우터를 FastAPI 앱에 연결!
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 테스트용으로 모든 출처 허용 (또는 ["http://localhost:5173"])
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def read_root():
    return {"message": "Server is running!"}

