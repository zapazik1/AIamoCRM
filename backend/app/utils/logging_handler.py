import logging
from io import StringIO
import datetime
from typing import List, Dict
import threading

# Синхронизированный список для хранения логов
class SynchronizedLogs:
    def __init__(self, max_entries=1000):
        self.logs: List[Dict] = []
        self.max_entries = max_entries
        self.lock = threading.Lock()
    
    def add(self, record):
        with self.lock:
            self.logs.append(record)
            # Сохраняем только последние max_entries записей
            if len(self.logs) > self.max_entries:
                self.logs = self.logs[-self.max_entries:]
    
    def get_all(self):
        with self.lock:
            return self.logs.copy()
    
    def clear(self):
        with self.lock:
            self.logs.clear()

# Создаем хранилище логов
memory_logs = SynchronizedLogs()

# Обработчик для хранения логов в памяти
class MemoryHandler(logging.Handler):
    def emit(self, record):
        try:
            # Форматируем сообщение и заменяем двойные переносы строк на одиночные
            message = self.format(record)
            # Избегаем дублирования времени и уровня в сообщении
            if message.startswith(record.levelname) or record.name in message.split(" - ", 1)[0]:
                # Если сообщение уже содержит форматированный префикс, используем только текст
                message_parts = message.split(" - ", 2)
                if len(message_parts) > 2:
                    message = message_parts[2]
            
            timestamp = datetime.datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')
            log_entry = {
                'timestamp': timestamp,
                'level': record.levelname,
                'logger': record.name,
                'message': message,
                'path': record.pathname,
                'line': record.lineno
            }
            memory_logs.add(log_entry)
        except Exception as e:
            self.handleError(record)
            print(f"Ошибка при обработке лога: {str(e)}")

# Функция для настройки логирования
def setup_logging():
    # Настройка форматирования
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Создание обработчика для вывода в консоль
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Создание обработчика для хранения в памяти
    memory_handler = MemoryHandler()
    memory_handler.setFormatter(formatter)
    
    # Настройка корневого логгера
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Добавление обработчиков к корневому логгеру
    root_logger.addHandler(console_handler)
    root_logger.addHandler(memory_handler)
    
    return root_logger 