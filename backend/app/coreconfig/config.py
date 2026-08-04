from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "OCR Project"
    debug: bool = True

settings = Settings()