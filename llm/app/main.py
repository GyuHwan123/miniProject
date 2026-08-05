from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # 1. CORS 모듈 임포트
from app.api.router import router

app = FastAPI()

# 2. 프론트엔드와 통신을 허용하기 위한 CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # 모든 출처(포트)에서의 요청 허용
    allow_credentials=True,     # 인증정보(쿠키 등) 포함 허용
    allow_methods=["*"],        # GET, POST 등 모든 HTTP 메서드 허용
    allow_headers=["*"],        # 모든 HTTP 헤더 허용
)

app.include_router(router)