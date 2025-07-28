from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.widget import router as widget_router
from app.api.logs import router as logs_router
from app.utils.logging_handler import setup_logging
import logging

# Настраиваем логирование
logger = setup_logging()
logger.info("Инициализация приложения")

# Создаем экземпляр FastAPI
app = FastAPI(
    title="AIamoCRM API",
    description="API для обработки сообщений виджета amoCRM",
    version="1.0.0"
)

# Настраиваем CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене заменить на конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(widget_router)
app.include_router(logs_router)

logger.info("Роутеры настроены")

# Корневой эндпоинт для проверки работоспособности
@app.get("/")
async def root():
    logger.info("Запрос на корневой эндпоинт")
    return {
        "status": "success",
        "message": "AIamoCRM API работает",
        "version": "1.0.0"
    }
