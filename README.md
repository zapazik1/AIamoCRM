# AI Assistant Widget for amoCRM

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.2-green.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-orange.svg)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20DB-purple.svg)

*Интеллектуальный AI-помощник для системы amoCRM с поддержкой русского языка*

</div>

## 🎯 О проекте

**AIamoCRM** - это умный виджет-помощник, который интегрируется в интерфейс amoCRM и предоставляет пользователям быстрые ответы на вопросы о функциональности системы, API и лучших практиках работы с CRM.

### Ключевые возможности

- 🤖 **Умная обработка запросов** - понимание естественного языка на русском
- 📚 **База знаний** - встроенная документация amoCRM и API референсы
- 💬 **Контекстные диалоги** - помнит историю разговора для связных ответов
- 🔄 **Интеграция в amoCRM** - работает прямо в интерфейсе CRM как виджет
- 🎛️ **Выбор моделей** - поддержка GPT-4o и GPT-4o-mini
- 🔍 **Семантический поиск** - находит релевантную информацию в документации

## 🏗️ Архитектура

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   amoCRM        │    │  FastAPI        │    │  OpenAI API     │
│   (Виджет)      │◄──►│  Backend        │◄──►│                 │
│                 │    │                 │    │ • GPT-4o        │
│ • UI виджета    │    │ • Обработка     │    │ • GPT-4o-mini   │
│ • Ввод запросов │    │ • Поиск в БЗ    │    │ • Эмбеддинги    │
│ • Вывод ответов │    │ • Управление    │    │                 │
│                 │    │   сессиями      │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   ChromaDB      │
                       │                 │
                       │ • База знаний   │
                       │ • Векторный     │
                       │   поиск         │
                       │ • 1000+ чанков  │
                       └─────────────────┘
```

## 🚀 Быстрый старт

### Требования

- **Python 3.11** (обязательно эта версия!)
- **OpenAI API Key**
- **Docker** (опционально)

### Установка

1. **Клонирование репозитория**
```bash
git clone https://github.com/yourusername/AIamoCRM.git
cd AIamoCRM
```

2. **Настройка окружения**
```bash
# Создание виртуального окружения
python3.11 -m venv venv
source venv/bin/activate  # Linux/Mac
# или
.\venv\Scripts\activate  # Windows

# Установка зависимостей
pip install -r backend/requirements.txt
```

3. **Конфигурация**
```bash
# Копирование примера конфигурации
cp .env.example .env

# Редактирование .env файла - добавьте ваш OpenAI API ключ
# OPENAI_API_KEY=sk-your-key-here
```

### Запуск

#### Режим разработки
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Docker
```bash
docker-compose up --build
```

API будет доступно по адресу: `http://localhost:8000`

## 📋 API Endpoints

| Метод | Путь | Описание |
|--------|------|----------|
| `POST` | `/api/widget/message` | Основной endpoint для обработки сообщений |
| `GET` | `/api/widget/models` | Список доступных AI моделей |
| `GET` | `/api/widget/health` | Проверка работоспособности |

### Пример запроса

```json
{
  "text": "Как создать сделку через API?",
  "user_id": 12345,
  "session_id": "user_12345",
  "model_name": "gpt-4o"
}
```

### Пример ответа

```json
{
  "status": "success",
  "message": "Для создания сделки используйте POST запрос на /api/v4/leads с параметрами...",
  "session_id": "user_12345"
}
```

## 🛠️ Технологический стек

### Backend
- **FastAPI** - современный Python веб-фреймворк
- **Pydantic** - валидация данных
- **OpenAI API** - интеграция с GPT моделями
- **ChromaDB** - векторная база данных
- **LangChain** - компоненты для LLM приложений

### Frontend
- **JavaScript** - разработка виджета для amoCRM
- **CSS3** - современные стили
- **amoCRM SDK** - интеграция с платформой

## 📁 Структура проекта

```
AIamoCRM/
├── backend/                # FastAPI приложение
│   ├── app/
│   │   ├── api/           # API endpoints
│   │   ├── services/      # Бизнес-логика
│   │   └── utils/         # Вспомогательные функции
│   └── requirements.txt
├── frontend_widget/       # amoCRM виджет
│   ├── script.js         # Основная логика виджета
│   ├── style.css         # Стили
│   └── manifest.json     # Конфигурация виджета
├── database/             # База знаний
│   ├── chunks/          # Обработанная документация
│   └── scripts/         # Скрипты обработки данных
└── docs/                # Техническая документация
```

## 📚 База знаний

Система включает обширную базу знаний, построенную на основе:
- Документации для разработчиков amoCRM
- API справочников
- Статей поддержки
- Руководств по лучшим практикам

**Характеристики:**
- 1000+ обработанных фрагментов документации
- Семантические эмбеддинги через OpenAI

## 🧪 Тестирование

```bash
# Тестирование API
curl -X POST "http://localhost:8000/api/widget/message" \
  -H "Content-Type: application/json" \
  -d '{"text": "Тестовый запрос", "target": "widget"}'
```

## 🚀 Деплой

### Docker деплой
```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

### Ручной деплой
```bash
# Установка зависимостей
pip install -r backend/requirements.txt

# Запуск с gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Railway деплой

Проект развернут на платформе [Railway](https://railway.app/). 

**Настройка:**
1. Подключите GitHub репозиторий к Railway
2. Добавьте переменные окружения в панели управления:
   ```
   OPENAI_API_KEY=sk-your-openai-api-key-here
   DEBUG=false
   SECRET_KEY=your-production-secret-key
   ```
3. Railway автоматически развернет приложение с HTTPS endpoint

**Продемонстрированные технологии:**
- Разработка backend на FastAPI
- Интеграция с OpenAI API  
- Реализация векторной базы данных
- Разработка виджетов для сторонних платформ
- Docker контейнеризация
- RESTful API дизайн



