from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Базовые настройки
    APP_NAME: str = "AIamoCRM"
    DEBUG: bool = True
    VERSION: str = "0.1.0"
    
    # Настройки API
    API_V1_STR: str = "/api/v1"
    
    # Настройки CORS
    CORS_ORIGINS: list = ["*"]
    
    # Настройки базы данных
    DATABASE_URL: str = "sqlite:///./app.db"
    
    # Настройки JWT
    SECRET_KEY: str = "your-secret-key"  # Заменить в продакшене
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
