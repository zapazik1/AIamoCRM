import os
import logging
import uuid
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()

# Глобальные переменные
_openai_client = None
_default_llm_model = os.getenv("LLM_MODEL", "gpt-4o")

# Список доступных моделей
AVAILABLE_MODELS = {
    "gpt-4o": "gpt-4o",
    "gpt-4o-mini": "gpt-4o-mini"
}

# Словарь для хранения истории диалогов
# Структура: {session_id: [{"role": role, "content": content, "timestamp": timestamp}, ...]}
_dialog_history = {}

def get_openai_client() -> OpenAI:
    """
    Инициализирует и возвращает клиент OpenAI.
    
    Returns:
        OpenAI: Клиент для работы с OpenAI API.
    
    Raises:
        ValueError: Если OPENAI_API_KEY не установлен.
    """
    global _openai_client
    
    if _openai_client is not None:
        logger.debug("Используется существующий клиент OpenAI")
        return _openai_client
    
    try:
        logger.info("Создание нового клиента OpenAI")
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Переменная окружения OPENAI_API_KEY не установлена.")
        
        client = OpenAI(api_key=api_key)
        logger.info("Клиент OpenAI успешно инициализирован.")
        _openai_client = client
        return client
    except Exception as e:
        logger.error(f"Ошибка инициализации клиента OpenAI: {e}")
        raise

def get_or_create_session(session_id: Optional[str] = None) -> str:
    """
    Получает существующую сессию или создает новую.
    
    Args:
        session_id: Идентификатор сессии. Если None, создается новый.
        
    Returns:
        str: Идентификатор сессии.
    """
    global _dialog_history
    
    if not session_id:
        # Создаем новый идентификатор сессии
        session_id = str(uuid.uuid4())
        logger.info(f"Создана новая сессия: {session_id}")
        _dialog_history[session_id] = []
    elif session_id not in _dialog_history:
        # Если сессия с таким ID не существует, создаем новую
        logger.info(f"Инициализирована сессия: {session_id}")
        _dialog_history[session_id] = []
        
    return session_id

def add_message_to_history(session_id: str, role: str, content: str) -> None:
    """
    Добавляет сообщение в историю диалога.
    
    Args:
        session_id: Идентификатор сессии.
        role: Роль отправителя (system, user, assistant).
        content: Содержимое сообщения.
    """
    global _dialog_history
    
    if session_id not in _dialog_history:
        get_or_create_session(session_id)
    
    message = {
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat()
    }
    
    _dialog_history[session_id].append(message)
    logger.debug(f"Добавлено сообщение в историю сессии {session_id}: {role}")

def get_session_history(session_id: str, max_messages: int = 10) -> List[Dict[str, str]]:
    """
    Получает историю диалога для сессии.
    
    Args:
        session_id: Идентификатор сессии.
        max_messages: Максимальное количество последних сообщений.
        
    Returns:
        List[Dict[str, str]]: Список сообщений в формате для API OpenAI.
    """
    global _dialog_history
    
    if session_id not in _dialog_history:
        return []
    
    # Получаем последние max_messages сообщений и форматируем для API
    messages = _dialog_history[session_id][-max_messages:]
    formatted_messages = [{"role": msg["role"], "content": msg["content"]} for msg in messages]
    
    return formatted_messages

def get_ai_response(
    user_query: str, 
    context_chunks: List[Dict[str, Any]], 
    system_instructions: Optional[str] = None,
    model_name: Optional[str] = None,
    session_id: Optional[str] = None,
    max_history_messages: int = 5
) -> str:
    """
    Отправляет запрос к API ChatGPT с учетом истории диалога и получает ответ от языковой модели.
    
    Args:
        user_query: Запрос пользователя.
        context_chunks: Список словарей с релевантными фрагментами контекста, 
                        каждый словарь должен содержать ключ 'text' с текстом чанка.
        system_instructions: Системные инструкции для языковой модели.
                            Если не указаны, используются стандартные инструкции.
        model_name: Название модели для использования (gpt-4o или gpt-4o-mini).
                   Если не указано, используется модель из .env файла.
        session_id: Идентификатор сессии для сохранения истории диалога.
        max_history_messages: Максимальное количество предыдущих сообщений для включения в контекст.
    
    Returns:
        str: Ответ от языковой модели.
    
    Raises:
        Exception: В случае ошибки при запросе к API.
    """
    try:
        # Получаем клиент OpenAI
        client = get_openai_client()
        
        # Получаем или создаем сессию
        current_session_id = get_or_create_session(session_id)
        
        # Выбираем модель на основе переданного параметра
        if model_name and model_name in AVAILABLE_MODELS:
            llm_model = AVAILABLE_MODELS[model_name]
            logger.info(f"Используется выбранная модель: {llm_model}")
        else:
            llm_model = _default_llm_model
            logger.info(f"Используется модель по умолчанию: {llm_model}")
        
        # Формируем контекст из найденных чанков
        context_text = ""
        for i, chunk in enumerate(context_chunks):
            if 'text' in chunk:
                chunk_text = chunk['text']
            elif 'document' in chunk:
                chunk_text = chunk['document']
            else:
                logger.warning(f"Чанк #{i} не содержит текста")
                continue
                
            context_text += f"\n\n--- Фрагмент {i+1} ---\n{chunk_text}"
        
        # Если системные инструкции не указаны, используем стандартные
        if system_instructions is None:
            system_instructions = """Ты - полезный ассистент amoCRM, который отвечает на вопросы пользователей о системе.
Используй информацию из предоставленного контекста для ответа.
Используй историю диалога с пользователем для понимания текущего вопроса.
Учитывай предыдущие вопросы и ответы при формулировании нового ответа.
Поддерживай последовательность в ответах, не противоречь предыдущим ответам.
Если пользователь ссылается на предыдущие части разговора, учитывай эту информацию.
Если в контексте нет ответа на новый вопрос, но ты уже отвечал на похожий вопрос в истории диалога, используй эту информацию.
Если ты не можешь найти ответ ни в контексте, ни в истории диалога, честно признайся, что не знаешь ответа, и предложи обратиться в службу поддержки amoCRM.
Не выдумывай информацию, которой нет ни в контексте, ни в истории диалога.
Отвечай кратко, но информативно.
Используй форматирование текста для улучшения читаемости, где это уместно."""
        
        # Получаем историю диалога
        history_messages = get_session_history(current_session_id, max_history_messages)
        
        # Если история пуста, добавляем системное сообщение
        if not history_messages:
            # Добавляем системное сообщение в историю
            add_message_to_history(current_session_id, "system", system_instructions)
            
            # Подготавливаем сообщение с контекстом и запросом
            user_message = f"Контекст:\n{context_text}\n\nВопрос пользователя:\n{user_query}"
            
            # Добавляем сообщение пользователя в историю
            add_message_to_history(current_session_id, "user", user_message)
            
            # Обновляем историю для сообщений API
            history_messages = get_session_history(current_session_id)
        else:
            # Если история уже есть, проверяем наличие системного сообщения
            if history_messages[0]["role"] != "system":
                # Если первое сообщение не системное, добавляем системное в начало
                add_message_to_history(current_session_id, "system", system_instructions)
                # Обновляем историю
                history_messages = get_session_history(current_session_id)
            
            # Добавляем новый запрос пользователя с контекстом
            user_message = f"Контекст:\n{context_text}\n\nВопрос пользователя:\n{user_query}"
            add_message_to_history(current_session_id, "user", user_message)
            
            # Обновляем историю
            history_messages = get_session_history(current_session_id)
        
        # Отправляем запрос к API с историей диалога
        logger.info(f"Отправка запроса с историей диалога к модели {llm_model}")
        response = client.chat.completions.create(
            model=llm_model,
            messages=history_messages,
            temperature=0.2  # Небольшая температура для более детерминированных ответов
        )
        
        # Получаем ответ
        ai_response = response.choices[0].message.content
        logger.info("Получен ответ от языковой модели")
        
        # Добавляем ответ в историю диалога
        add_message_to_history(current_session_id, "assistant", ai_response)
        
        return ai_response
        
    except Exception as e:
        logger.error(f"Ошибка при получении ответа от языковой модели: {e}")
        # В зависимости от требований, можно вернуть сообщение об ошибке или пробросить исключение дальше
        return f"Произошла ошибка при получении ответа: {str(e)}"
