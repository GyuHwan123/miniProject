from fastapi import FastAPI
from app.api.router import router as api_router

app = FastAPI(title="OCR & LLM Project")

# ⭕ 만드신 라우터를 FastAPI 앱에 연결!
app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "Server is running!"}