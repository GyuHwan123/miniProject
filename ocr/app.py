
from fastapi import FastAPI
from router import router

app = FastAPI()

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8002,
        reload=False,
        workers=1
    )