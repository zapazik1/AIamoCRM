from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import os
from pathlib import Path
from app.utils.logging_handler import memory_logs

# Создаем роутер для логов
router = APIRouter(prefix="/api/logs", tags=["logs"])

# Определяем директорию для шаблонов (на один уровень выше текущего файла)
base_dir = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(base_dir / "templates"))

# Обработчик для страницы с логами
@router.get("/viewer", response_class=HTMLResponse)
async def get_logs_page(request: Request):
    """
    Отображает HTML страницу с логами
    """
    return templates.TemplateResponse("logs.html", {"request": request})

# API для получения списка логов
@router.get("/")
async def get_logs():
    """
    Возвращает список логов в JSON формате
    """
    return memory_logs.get_all()

# API для очистки логов
@router.post("/clear")
async def clear_logs():
    """
    Очищает список логов
    """
    memory_logs.clear()
    return {"success": True, "message": "Логи очищены"} 