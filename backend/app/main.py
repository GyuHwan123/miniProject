from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import router as api_router

app = FastAPI(title="OCR & LLM Project")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,   # 중요!
    allow_methods=["*"],
    allow_headers=["*"],
)
# ⭕ 만드신 라우터를 FastAPI 앱에 연결!
app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "Server is running!"}

