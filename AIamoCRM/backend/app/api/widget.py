from fastapi import APIRouter, HTTPException, Depends, Request, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging
import traceback
import json
import requests
from app.services.test_retrieval import retrieve_amocrm_context
from app.services.get_ai_response import get_ai_response, AVAILABLE_MODELS, get_or_create_session
# Настройка логирования для отслеживания работы API
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Создаем роутер с префиксом /api/widget
router = APIRouter(prefix="/api/widget", tags=["widget"], responses={404: {"description": "Not found"}})

class WidgetMessage(BaseModel):
    """Модель для входящих сообщений от виджета"""
    text: str
    user_id: Optional[int] = None
    contact_id: Optional[int] = None
    lead_id: Optional[int] = None
    account_id: Optional[int] = None
    target: str
    model_name: Optional[str] = None
    session_id: Optional[str] = None
    
class WidgetResponse(BaseModel):
    """Модель для ответа виджету"""
    status: str
    message: str

@router.post("/message", response_model=WidgetResponse)
async def process_widget_message(request: Request):
    """
    Обрабатывает входящие сообщения от чат-виджета.
    
    Args:
        request: FastAPI Request объект, содержащий данные запроса
        
    Returns:
        JSONResponse: Ответ сервера с результатом обработки сообщения
        
    Raises:
        HTTPException: Если произошла ошибка при обработке запроса
    """
    try:
        # Получаем информацию о клиенте
        client_host = request.client.host if request.client else "unknown"
        logger.info(f"Получен запрос от {client_host}")
        logger.info(f"Заголовки запроса: {dict(request.headers)}")
        
        # Получаем сырые данные из тела запросач
        raw_data = await request.body()
        logger.info(f"Получены сырые данные: {raw_data}") 
        
        # Определяем тип контента
        content_type = request.headers.get('content-type', '').lower()
        logger.info(f"Content-Type: {content_type}")
        
        # Данные для Pydantic модели
        data = {}
        
        # Обрабатываем данные в зависимости от типа контента
        if 'application/json' in content_type:
            # JSON данные
            try:
                data = json.loads(raw_data)
                logger.info(f"Распарсенные JSON данные: {data}")
            except json.JSONDecodeError as e:
                logger.error(f"Ошибка парсинга JSON: {str(e)}")
                return JSONResponse(
                    status_code=400,
                    content={
                        "status": "error",
                        "message": "Неверный формат JSON данных",
                        "details": str(e)
                    }
                )
        elif 'application/x-www-form-urlencoded' in content_type or 'multipart/form-data' in content_type:
            # Form данные
            try:
                form = await request.form()
                logger.info(f"Получены form-данные: {form}")
                # Преобразуем form-данные в словарь
                data = dict(form)
                logger.info(f"Form-данные в виде словаря: {data}")
            except Exception as e:
                logger.error(f"Ошибка при обработке form-данных: {str(e)}")
                return JSONResponse(
                    status_code=400,
                    content={
                        "status": "error",
                        "message": "Ошибка при обработке form-данных",
                        "details": str(e)
                    }
                )
        else:
            # Пробуем как JSON, потом как обычный текст
            try:
                data = json.loads(raw_data)
                logger.info(f"Распарсенные данные из неизвестного типа: {data}")
            except json.JSONDecodeError:
                # Пробуем как обычный текст
                try:
                    text = raw_data.decode('utf-8')
                    logger.info(f"Получен обычный текст: {text}")
                    data = {"text": text}
                except UnicodeDecodeError as e:
                    logger.error(f"Ошибка декодирования данных: {str(e)}")
                    return JSONResponse(
                        status_code=400,
                        content={
                            "status": "error",
                            "message": "Неизвестный формат данных",
                            "details": "Невозможно декодировать как UTF-8"
                        }
                    )
        
        # Валидируем данные с помощью Pydantic модели
        try:
            # Если есть только текст, установим target по умолчанию
            if 'text' in data and 'target' not in data:
                data['target'] = 'widget'
                
            logger.info(f"Подготовленные данные для валидации: {data}")
            message = WidgetMessage(**data)
            logger.info(f"Валидированные данные: {message.dict()}")
        except Exception as e:
            logger.error(f"Ошибка валидации данных: {str(e)}")
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Неверный формат данных",
                    "details": str(e)
                }
            )
        
        # Получаем релевантные чанки из базы знаний
        retrieved_chunks = retrieve_amocrm_context(message.text, top_k=5)
        logger.info(f"Найдено {len(retrieved_chunks)} релевантных чанков")

        # Проверяем валидность модели, если указана
        model_name = None
        if message.model_name:
            if message.model_name in AVAILABLE_MODELS:
                model_name = message.model_name
                logger.info(f"Используется выбранная пользователем модель: {model_name}")
            else:
                logger.warning(f"Запрошена неподдерживаемая модель: {message.model_name}. Будет использована модель по умолчанию.")

        # Получаем или генерируем ID сессии
        session_id = message.session_id
        if not session_id:
            # Если ID сессии не указан, генерируем новый или используем user_id/contact_id
            if message.user_id:
                session_id = f"user_{message.user_id}"
            elif message.contact_id:
                session_id = f"contact_{message.contact_id}"
            else:
                # Создаем новую случайную сессию
                session_id = get_or_create_session()
                
        logger.info(f"Используется ID сессии: {session_id}")

        # Генерируем ответ с помощью AI
        system_instructions = """Ты - полезный ассистент amoCRM, который отвечает на вопросы пользователей о системе.
Используй информацию из предоставленного контекста для ответа.
Используй историю диалога с пользователем для понимания текущего вопроса.
Учитывай предыдущие вопросы и ответы при формулировании нового ответа.
Поддерживай последовательность в ответах, не противоречь предыдущим ответам.
Если пользователь ссылается на предыдущие части разговора, учитывай эту информацию.
Если в контексте нет ответа на новый вопрос, но ты уже отвечал на похожий вопрос в истории диалога, используй эту информацию.
Если ты не можешь найти ответ ни в контексте, ни в истории диалога, честно признайся, что не знаешь ответа, и предложи обратиться в службу поддержки amoCRM.
Не выдумывай информацию, которой нет ни в контексте, ни в истории диалога.
Отвечай кратко, но информативно."""

        ai_response = get_ai_response(
            user_query=message.text,
            context_chunks=retrieved_chunks,
            system_instructions=system_instructions,
            model_name=model_name,
            session_id=session_id
        )
        
        # Возвращаем успешный ответ
        response_data = {
            "status": "success",
            "message": ai_response,
            "session_id": session_id
        }
        logger.info(f"Отправляем ответ: {response_data}")
        
        return JSONResponse(
            status_code=200,
            content=response_data
        )
        
    except Exception as e:
        # Обработка всех остальных ошибок
        logger.error(f"Неожиданная ошибка: {str(e)}")
        logger.error(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": "Внутренняя ошибка сервера",
                "details": str(e)
            }
        )

@router.post("/message/form")
async def process_widget_message_form(
    request: Request,
    text: str = Form(...),
    user_id: Optional[str] = Form(None),
    model_name: Optional[str] = Form(None),
    session_id: Optional[str] = Form(None)
):
    """
    Обработка сообщения от виджета amoCRM в формате form-data
    """
    try:
        # Логируем полученные данные
        form_data = await request.form()
        logger.info(f"Получены form-data: {dict(form_data)}")
        
        # Создаем объект сообщения
        message = WidgetMessage(
            text=text,
            user_id=user_id,
            target="widget",
            model_name=model_name,
            session_id=session_id
        )
        
        # Получаем релевантные чанки из базы знаний
        retrieved_chunks = retrieve_amocrm_context(message.text, top_k=5)
        logger.info(f"Найдено {len(retrieved_chunks)} релевантных чанков")
        
        # Проверяем валидность модели
        selected_model = None
        if model_name and model_name in AVAILABLE_MODELS:
            selected_model = model_name
            logger.info(f"Используется выбранная пользователем модель: {selected_model}")
        else:
            logger.info("Используется модель по умолчанию")
        
        # Получаем или генерируем ID сессии
        if not session_id:
            # Если ID сессии не указан, генерируем новый или используем user_id
            if user_id:
                session_id = f"user_{user_id}"
            else:
                # Создаем новую случайную сессию
                session_id = get_or_create_session()
                
        logger.info(f"Используется ID сессии: {session_id}")
        
        # Генерируем ответ с помощью AI
        system_instructions = """Ты - полезный ассистент amoCRM, который отвечает на вопросы пользователей о системе.
Используй информацию из предоставленного контекста для ответа.
Используй историю диалога с пользователем для понимания текущего вопроса.
Учитывай предыдущие вопросы и ответы при формулировании нового ответа.
Поддерживай последовательность в ответах, не противоречь предыдущим ответам.
Если пользователь ссылается на предыдущие части разговора, учитывай эту информацию.
Если в контексте нет ответа на новый вопрос, но ты уже отвечал на похожий вопрос в истории диалога, используй эту информацию.
Если ты не можешь найти ответ ни в контексте, ни в истории диалога, честно признайся, что не знаешь ответа, и предложи обратиться в службу поддержки amoCRM.
Не выдумывай информацию, которой нет ни в контексте, ни в истории диалога.
Отвечай кратко, но информативно."""

        ai_response = get_ai_response(
            user_query=message.text,
            context_chunks=retrieved_chunks,
            system_instructions=system_instructions,
            model_name=selected_model,
            session_id=session_id
        )
        
        # Возвращаем ответ
        response = {
            "status": "success",
            "message": ai_response,
            "session_id": session_id
        }
        logger.info(f"Отправляем ответ: {response}")
        return JSONResponse(content=response)
        
    except Exception as e:
        logger.error(f"Ошибка при обработке сообщения: {str(e)}")
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": f"Ошибка: {str(e)}"
            }
        )

@router.get("/health", response_model=Dict[str, str])
async def widget_health_check():
    """
    Проверка работоспособности API виджета
    """
    logger.info("Запрос на проверку работоспособности API виджета")
    return {"status": "Widget API is working"}

@router.post("/", response_model=WidgetResponse)
async def root_widget_message(request: Request):
    """
    Обработчик для корневого маршрута /api/v1/widget/
    Этот эндпоинт нужен для тестирования, если виджет посылает запросы на корневой URL
    """
    try:
        # Получаем сырые данные запроса
        raw_body = await request.body()
        content_type = request.headers.get('content-type', '')
        
        logger.info(f"Получен запрос на корневой URL. Content-Type: {content_type}")
        logger.info(f"Сырые данные запроса: {raw_body}")
        
        # Пытаемся разобрать данные в зависимости от формата
        text = ""
        model_name = None
        session_id = None
        
        if 'application/json' in content_type:
            try:
                body = await request.json()
                logger.info(f"Получен JSON: {body}")
                text = body.get("text", "неизвестное сообщение")
                model_name = body.get("model_name")
                session_id = body.get("session_id")
            except:
                logger.error("Ошибка при парсинге JSON")
                text = "неизвестное сообщение (ошибка парсинга JSON)"
        elif 'application/x-www-form-urlencoded' in content_type:
            try:
                form_data = await request.form()
                logger.info(f"Получены form-data: {form_data}")
                text = form_data.get("text", "неизвестное сообщение")
                model_name = form_data.get("model_name")
                session_id = form_data.get("session_id")
            except:
                logger.error("Ошибка при парсинге form-data")
                text = "неизвестное сообщение (ошибка парсинга form-data)"
        else:
            text = raw_body.decode('utf-8', errors='ignore')
            logger.info(f"Получены сырые данные: {text}")
            
        # Получаем релевантные чанки из базы знаний
        retrieved_chunks = retrieve_amocrm_context(text, top_k=5)
        logger.info(f"Найдено {len(retrieved_chunks)} релевантных чанков")
        
        # Проверяем валидность модели
        if model_name and model_name in AVAILABLE_MODELS:
            logger.info(f"Используется выбранная пользователем модель: {model_name}")
        else:
            model_name = None
            logger.info("Используется модель по умолчанию")
            
        # Получаем или генерируем ID сессии
        if not session_id:
            # Создаем новую случайную сессию
            session_id = get_or_create_session()
                
        logger.info(f"Используется ID сессии: {session_id}")
        
        # Генерируем ответ с помощью AI
        system_instructions = """Ты - полезный ассистент amoCRM, который отвечает на вопросы пользователей о системе.
Используй информацию из предоставленного контекста для ответа.
Используй историю диалога с пользователем для понимания текущего вопроса.
Учитывай предыдущие вопросы и ответы при формулировании нового ответа.
Поддерживай последовательность в ответах, не противоречь предыдущим ответам.
Если пользователь ссылается на предыдущие части разговора, учитывай эту информацию.
Если в контексте нет ответа на новый вопрос, но ты уже отвечал на похожий вопрос в истории диалога, используй эту информацию.
Если ты не можешь найти ответ ни в контексте, ни в истории диалога, честно признайся, что не знаешь ответа, и предложи обратиться в службу поддержки amoCRM.
Не выдумывай информацию, которой нет ни в контексте, ни в истории диалога.
Отвечай кратко, но информативно."""

        ai_response = get_ai_response(
            user_query=text,
            context_chunks=retrieved_chunks,
            model_name=model_name,
            session_id=session_id
        )
            
        # Формируем и возвращаем ответ
        response = {
            "status": "success",
            "message": ai_response,
            "session_id": session_id
        }
        logger.info(f"Отправляем ответ: {response}")
        return response
    except Exception as e:
        logger.error(f"Ошибка при обработке запроса на корневом URL: {str(e)}")
        return {
            "status": "error",
            "message": f"Произошла ошибка: {str(e)}"
        } 

@router.get("/models", response_model=Dict[str, Any])
async def get_available_models():
    """
    Возвращает список доступных моделей LLM для выбора в виджете
    """
    logger.info("Запрос на получение списка доступных моделей")
    
    try:
        # Преобразуем словарь моделей в формат для фронтенда
        models_list = [
            {"id": model_id, "name": model_name, "description": get_model_description(model_id)}
            for model_id, model_name in AVAILABLE_MODELS.items()
        ]
        
        response = {
            "status": "success",
            "models": models_list
        }
        
        logger.info(f"Отправляем список моделей: {response}")
        return response
    except Exception as e:
        logger.error(f"Ошибка при получении списка моделей: {str(e)}")
        return {
            "status": "error",
            "message": f"Ошибка при получении списка моделей: {str(e)}"
        }

def get_model_description(model_id: str) -> str:
    """
    Возвращает описание модели по её идентификатору
    
    Args:
        model_id: Идентификатор модели
        
    Returns:
        str: Описание модели
    """
    descriptions = {
        "gpt-4o": "GPT-4o - мощная модель с широкими возможностями и высоким качеством ответов",
        "gpt-4o-mini": "GPT-4o-mini - более быстрая и экономичная версия с хорошим балансом качества и производительности"
    }
    
    return descriptions.get(model_id, "Нет описания") 