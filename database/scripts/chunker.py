#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
import json
import re
import hashlib
import time # Импортируем time для замера
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple, Set

from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

# Определение заголовков для MarkdownHeaderTextSplitter
HEADERS_TO_SPLIT_ON = [
    ("#", "header_1"),
    ("##", "header_2"),
    ("###", "header_3"),
    ("####", "header_4"),
    ("#####", "header_5"),
    ("######", "header_6"),
]

# Список бизнес-сущностей amoCRM
ENTITY_TYPES = {
    "lead": ["сделка", "сделки", "сделок", "лид", "лиды", "лидов"],
    "contact": ["контакт", "контакты", "контактов", "клиент", "клиенты", "клиентов"],
    "company": ["компания", "компании", "компаний", "организация", "организации", "организаций"],
    "customer": ["покупатель", "покупатели", "покупателей", "customer", "customers"],
    "task": ["задача", "задачи", "задач", "task", "tasks"],
    "catalog": ["каталог", "каталоги", "каталогов", "список", "списки", "списков", "catalog", "catalogs"],
    "pipeline": ["воронка", "воронки", "воронок", "pipeline", "pipelines"]
}

# Ключевые методы API
API_METHOD_PATTERNS = [
    r'(GET|POST|PUT|DELETE|PATCH)\s+([/a-zA-Z0-9_\-]+)',
    r'(Создание|Получение|Редактирование|Изменение|Удаление)\s+([а-яА-Я\s]+)'
]

def detect_document_type(file_path: str, content: Optional[str] = None) -> str:
    """
    Определяет тип документации на основе пути файла и содержимого.
    
    Args:
        file_path: Путь к файлу
        content: Содержимое файла (опционально, для более точного определения)
        
    Returns:
        Строка: "api", "support", "faq", "tutorial" или "general"
    """
    file_path_lower = file_path.lower()
    
    # Определение по пути файла
    if "developers" in file_path_lower or "api" in file_path_lower:
        doc_type = "api"
    elif "support" in file_path_lower:
        if "faq" in file_path_lower:
            doc_type = "faq"
        elif "tutorial" in file_path_lower or "howto" in file_path_lower:
            doc_type = "tutorial"
        else:
            doc_type = "support"
    else:
        doc_type = "general"
    
    # Уточнение по содержимому, если предоставлено
    if content:
        # Признаки API документации
        if re.search(r'(GET|POST|PUT|DELETE|PATCH)\s+[^\s]+', content):
            doc_type = "api"
        # Признаки FAQ
        elif is_faq_content(content):
            doc_type = "faq"
        # Признаки пошаговой инструкции
        elif is_step_by_step_content(content):
            doc_type = "tutorial"
    
    return doc_type

def extract_breadcrumbs(metadata: Dict[str, Any]) -> str:
    """
    Создает строку breadcrumbs из метаданных заголовков.
    
    Args:
        metadata: Словарь метаданных с заголовками
        
    Returns:
        Строка с путем заголовков, разделенных " > "
    """
    breadcrumbs = []
    
    # Добавляем заголовок документа, если есть
    if "title" in metadata and metadata["title"]:
        breadcrumbs.append(metadata["title"])
    
    # Добавляем все заголовки по порядку
    for i in range(1, 7):
        header_key = f"header_{i}"
        if header_key in metadata and metadata[header_key]:
            breadcrumbs.append(metadata[header_key])
    
    return " > ".join(breadcrumbs)

def normalize_phone_number(text: str) -> str:
    """
    Нормализует телефонные номера в тексте для единообразного представления.
    
    Args:
        text: Текст для обработки
        
    Returns:
        Текст с нормализованными телефонными номерами
    """
    # Ищем телефоны в формате +7 (XXX) XXX-XX-XX или 8 (XXX) XXX-XX-XX и т.д.
    phone_patterns = [
        r'(\+7|\b8)[\s\(]*(\d{3})[\s\)]*(\d{3})[\s\-]*(\d{2})[\s\-]*(\d{2})',
        r'(\+\d{1,3}|\b\d{1})[\s\(]*(\d{3,4})[\s\)]*(\d{3})[\s\-]*(\d{4})',
    ]
    
    normalized_text = text
    for pattern in phone_patterns:
        def phone_replace(match):
            # Нормализуем телефон к виду +7XXXXXXXXXX
            groups = match.groups()
            country_code = groups[0].replace('8', '+7')
            if not country_code.startswith('+'):
                country_code = '+' + country_code
            return f"{country_code}{groups[1]}{groups[2]}{groups[3]}{groups[4] if len(groups) > 4 else ''}"
        
        normalized_text = re.sub(pattern, phone_replace, normalized_text)
    
    return normalized_text

def cleanup_markdown_artifacts(text: str) -> str:
    """
    Очищает текст от артефактов разметки Markdown, которые могут затруднять понимание.
    
    Args:
        text: Текст для очистки
        
    Returns:
        Очищенный текст
    """
    # Заменяем незакрытые маркдаун-ссылки на просто текст
    text = re.sub(r'\[([^\]]+)\](?!\()', r'\1', text)
    
    # Заменяем незакрытые маркдаун-вставки кода на обычный текст
    text = re.sub(r'`([^`]+)(?!`)', r'\1', text)
    
    # Заменяем экранированные символы на обычные
    text = re.sub(r'\\([\\`*_{}[\]()#+-.!])', r'\1', text)
    
    return text

def fix_code_blocks(text: str) -> str:
    """
    Исправляет проблемы с форматированием кода в markdown.
    
    Args:
        text: Текст для обработки
        
    Returns:
        Исправленный текст с корректно оформленными блоками кода
    """
    # Находим все блоки кода
    code_blocks = re.findall(r'```[^`]*```', text, re.DOTALL)
    
    for block in code_blocks:
        # Исправляем экранированные слэши в curl командах и других кодах
        fixed_block = block.replace('\\_', '_').replace('\\\\', '\\')
        
        # Заменяем блок на исправленный
        text = text.replace(block, fixed_block)
    
    return text

def fix_url_paths(text: str) -> str:
    """
    Исправляет проблемы с URL-путями в тексте.
    
    Args:
        text: Текст для обработки
        
    Returns:
        Текст с исправленными URL-путями
    """
    # Находим сломанные URL-пути и исправляем их
    # 1. Исправляем относительные URL в markdown-ссылках
    text = re.sub(r'\]\((/[^\)]+)\)', r'](https://www.amocrm.ru\1)', text)
    
    # 2. Исправляем двойные ссылки (проблемные URL в amoCRM документации)
    text = re.sub(r'(https?://[^\s]+)(https?://)', r'\1 \2', text)
    
    return text

def create_metadata_prefixes(doc_type: str, metadata: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    """
    Создает метаданные для чанка вместо текстовых префиксов.
    
    Args:
        doc_type: Тип документа ("api", "support", "faq", "tutorial", "general")
        metadata: Словарь метаданных
        
    Returns:
        Кортеж из строки с кратким контекстом и дополненного словаря метаданных
    """
    additional_metadata = {}
    context_prefix = ""
    
    # Добавляем тип документа в метаданные
    additional_metadata["doc_type"] = doc_type
    
    # Для API документации добавляем больше контекста
    if doc_type == "api":
        # Если это метод API, добавляем информацию о нем
        if "header_3" in metadata and metadata["header_3"]:
            header = metadata["header_3"]
            # Проверяем типичные названия методов API
            if any(keyword in header.lower() for keyword in ["создание", "получение", "редактирование", "удаление", "добавление", "обновление"]):
                if "header_4" in metadata and metadata["header_4"]:
                    additional_metadata["api_method"] = f"{header} - {metadata['header_4']}"
                    context_prefix = f"API Метод: {header} - {metadata['header_4']}\n\n"
                else:
                    additional_metadata["api_method"] = header
                    context_prefix = f"API Метод: {header}\n\n"
    
    # Для документации типа FAQ или инструкции
    elif doc_type in ["faq", "tutorial"]:
        additional_metadata["content_structure"] = doc_type
        if "header_2" in metadata and metadata["header_2"]:
            additional_metadata["main_topic"] = metadata["header_2"]
    
    return context_prefix, additional_metadata

def process_code_blocks(text: str) -> List[Dict[str, Any]]:
    """
    Извлекает блоки кода из текста для отдельной обработки.
    
    Args:
        text: Текст для обработки
        
    Returns:
        Список словарей с информацией о блоке кода
    """
    code_blocks = []
    
    # Находим все блоки кода с указанием языка и без
    code_pattern = r'```([a-zA-Z0-9]*)\n(.*?)```'
    matches = re.finditer(code_pattern, text, re.DOTALL)
    
    for i, match in enumerate(matches):
        lang, code = match.groups()
        
        # Очищаем и нормализуем код
        cleaned_code = code.strip()
        # Исправляем экранированные слэши и другие проблемы с форматированием
        cleaned_code = cleaned_code.replace('\\_', '_').replace('\\\\', '\\')
        
        code_blocks.append({
            "id": i,
            "lang": lang.strip(),
            "code": cleaned_code,
            "start": match.start(),
            "end": match.end()
        })
    
    return code_blocks

def process_tables(text: str) -> List[Dict[str, Any]]:
    """
    Извлекает таблицы из текста для отдельной обработки.
    
    Args:
        text: Текст для обработки
        
    Returns:
        Список словарей с информацией о таблице
    """
    tables = []
    
    # Находим все markdown-таблицы (учитываем заголовок, разделитель и строки данных)
    table_pattern = r'(\|[^\n]+\|\n\|[\s\-:]+\|\n(?:\|[^\n]+\|\n)+)'
    matches = re.finditer(table_pattern, text, re.DOTALL)
    
    for i, match in enumerate(matches):
        table_text = match.group(1)
        
        tables.append({
            "id": i,
            "table": table_text.strip(),
            "start": match.start(),
            "end": match.end()
        })
    
    return tables

def process_api_documentation(
    text: str, 
    metadata: Dict[str, Any],
    chunk_size: int = 1500,  # Увеличено с 800
    chunk_overlap: int = 200  # Увеличено со 100
) -> List[Dict[str, Any]]:
    """
    Специализированная обработка для API документации.
    
    Args:
        text: Текст для обработки
        metadata: Дополнительные метаданные
        chunk_size: Целевой размер чанка
        chunk_overlap: Перекрытие между чанками
        
    Returns:
        Список словарей с чанками
    """
    chunks = []
    
    # Добавляем контекстный префикс и обновляем метаданные
    context_prefix, additional_metadata = create_metadata_prefixes("api", metadata)
    updated_metadata = {**metadata, **additional_metadata}
    
    # Ищем пары запрос-ответ API
    api_pairs = find_request_response_pairs(text)
    
    # Ищем таблицы параметров
    tables = process_tables(text)
    
    # Ищем блоки кода
    code_blocks = process_code_blocks(text)
    
    # Если нашли пары запрос-ответ, обрабатываем их вместе
    if api_pairs:
        # Создаем копию текста для маркировки
        marked_text = text
        
        # Заменяем пары запрос-ответ маркерами
        for i, pair in enumerate(api_pairs):
            req_start = marked_text.find(pair["request"])
            resp_start = marked_text.find(pair["response"])
            
            if req_start >= 0 and resp_start >= 0:
                # Определяем конец сегмента (наибольший из концов запроса и ответа)
                req_end = req_start + len(pair["request"])
                resp_end = resp_start + len(pair["response"])
                pair_end = max(req_end, resp_end)
                
                # Если запрос идет перед ответом
                if req_start < resp_start:
                    # Заменяем весь сегмент от начала запроса до конца ответа маркером
                    pair_text = marked_text[req_start:pair_end]
                    marked_text = marked_text[:req_start] + f"[[API_PAIR_{i}]]" + marked_text[pair_end:]
                else:
                    # Если ответ перед запросом (нестандартная ситуация)
                    pair_text = marked_text[resp_start:pair_end]
                    marked_text = marked_text[:resp_start] + f"[[API_PAIR_{i}]]" + marked_text[pair_end:]
                
                # Сохраняем текст пары для последующего восстановления
                pair["full_text"] = pair_text
        
        # Дополнительно заменяем оставшиеся блоки кода маркерами
        for block in code_blocks:
            # Пропускаем блоки, которые уже были заменены как часть пар запрос-ответ
            block_pos = marked_text.find(block["code"])
            if block_pos >= 0:
                marked_text = marked_text[:block_pos-4] + f"[[CODE_BLOCK_{block['id']}]]" + marked_text[block_pos + len(block["code"])+4:]
        
        # Дополнительно заменяем оставшиеся таблицы маркерами
        for table in tables:
            # Пропускаем таблицы, которые уже были заменены как часть пар запрос-ответ
            table_pos = marked_text.find(table["table"])
            if table_pos >= 0:
                marked_text = marked_text[:table_pos] + f"[[TABLE_{table['id']}]]" + marked_text[table_pos + len(table["table"]):]
        
        # Разбиваем текст на фрагменты с увеличенным размером чанка
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n## ", "\n### ", "\n#### ", "\n\n", "\n", ". ", "! ", "? ", ";", ":", " ", ""],
            keep_separator=True
        )
        splits = splitter.split_text(marked_text)
        
        # Восстанавливаем маркеры
        for split in splits:
            restored_split = split
            
            # Восстанавливаем пары запрос-ответ
            for i, pair in enumerate(api_pairs):
                if f"[[API_PAIR_{i}]]" in restored_split:
                    restored_split = restored_split.replace(f"[[API_PAIR_{i}]]", pair["full_text"])
            
            # Восстанавливаем блоки кода
            for block in code_blocks:
                if f"[[CODE_BLOCK_{block['id']}]]" in restored_split:
                    code_block = f"```{block['lang']}\n{block['code']}\n```"
                    restored_split = restored_split.replace(f"[[CODE_BLOCK_{block['id']}]]", code_block)
            
            # Восстанавливаем таблицы
            for table in tables:
                if f"[[TABLE_{table['id']}]]" in restored_split:
                    restored_split = restored_split.replace(f"[[TABLE_{table['id']}]]", table["table"])
            
            # Применяем обработку текста
            restored_split = fix_url_paths(restored_split)
            restored_split = normalize_phone_number(restored_split)
            restored_split = cleanup_markdown_artifacts(restored_split)
            
            # Увеличиваем минимальный размер чанка до 60 слов для API (было 40)
            if len(restored_split.split()) >= 60:
                # Извлекаем ключевые термины для метаданных (но не добавляем в текст)
                key_terms = extract_key_terms(restored_split, "api")
                chunk_metadata = updated_metadata.copy()
                if key_terms:
                    chunk_metadata["key_terms"] = key_terms
                
                chunks.append({
                    "text": context_prefix + restored_split,
                    "metadata": chunk_metadata
                })
    else:
        # Если нет пар запрос-ответ, обрабатываем таблицы и блоки кода отдельно
        
        # Создаем копию текста для маркировки
        marked_text = text
        
        # Заменяем таблицы маркерами
        for table in tables:
            marked_text = marked_text[:table["start"]] + f"[[TABLE_{table['id']}]]" + marked_text[table["end"]:]
        
        # Заменяем блоки кода маркерами
        for block in code_blocks:
            # Учитываем смещение позиций из-за замены таблиц
            block_start = block["start"]
            block_end = block["end"]
            for table in tables:
                if table["start"] < block_start:
                    offset = len(f"[[TABLE_{table['id']}]]") - (table["end"] - table["start"])
                    block_start += offset
                    block_end += offset
            
            marked_text = marked_text[:block_start] + f"[[CODE_BLOCK_{block['id']}]]" + marked_text[block_end:]
        
        # Разбиваем текст на фрагменты с увеличенным размером чанка
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n## ", "\n### ", "\n#### ", "\n\n", "\n", ". ", "! ", "? ", ";", ":", " ", ""],
            keep_separator=True
        )
        splits = splitter.split_text(marked_text)
        
        # Восстанавливаем маркеры
        for split in splits:
            restored_split = split
            
            # Восстанавливаем таблицы
            for table in tables:
                if f"[[TABLE_{table['id']}]]" in restored_split:
                    restored_split = restored_split.replace(f"[[TABLE_{table['id']}]]", table["table"])
            
            # Восстанавливаем блоки кода
            for block in code_blocks:
                if f"[[CODE_BLOCK_{block['id']}]]" in restored_split:
                    code_block = f"```{block['lang']}\n{block['code']}\n```"
                    restored_split = restored_split.replace(f"[[CODE_BLOCK_{block['id']}]]", code_block)
            
            # Применяем обработку текста
            restored_split = fix_url_paths(restored_split)
            restored_split = normalize_phone_number(restored_split)
            restored_split = cleanup_markdown_artifacts(restored_split)
            
            # Увеличиваем минимальный размер чанка до 60 слов для API (было 40)
            if len(restored_split.split()) >= 60:  # Было 40
                # Извлекаем ключевые термины для метаданных (но не добавляем в текст)
                key_terms = extract_key_terms(restored_split, "api")
                chunk_metadata = updated_metadata.copy()
                if key_terms:
                    chunk_metadata["key_terms"] = key_terms
                
                chunks.append({
                    "text": context_prefix + restored_split,
                    "metadata": chunk_metadata
                })
    
    return chunks

def is_step_by_step_content(text: str) -> bool:
    """
    Проверяет, является ли текст пошаговой инструкцией.
    
    Args:
        text: Текст для проверки
        
    Returns:
        True, если текст содержит пошаговые инструкции
    """
    step_patterns = [
        r'\d+\.\s+[А-Яа-я]',  # 1. Шаг
        r'Шаг \d+:',           # Шаг 1:
        r'Сначала [а-я]',      # Сначала сделайте...
        r'Затем [а-я]',        # Затем выполните...
        r'После этого [а-я]',  # После этого...
        r'В конце [а-я]',      # В конце...
        r'Наконец,',           # Наконец,...
    ]
    
    for pattern in step_patterns:
        if re.search(pattern, text):
            return True
            
    # Проверяем наличие нескольких последовательных нумерованных строк
    numbered_lines = re.findall(r'^\s*\d+\.\s+[^\n]+', text, re.MULTILINE)
    if len(numbered_lines) >= 2:
        return True
        
    return False

def is_faq_content(text: str) -> bool:
    """
    Проверяет, является ли текст FAQ.
    
    Args:
        text: Текст для проверки
        
    Returns:
        True, если текст содержит вопросы-ответы
    """
    # Ищем характерные вопросительные конструкции
    question_patterns = [
        r'(?:Как|Почему|Где|Когда|Что такое|Зачем)[^\.]+\?',
        r'^[^\.]+\?\s*$'  # Строка, заканчивающаяся вопросительным знаком
    ]
    
    question_count = 0
    for pattern in question_patterns:
        questions = re.findall(pattern, text, re.MULTILINE)
        question_count += len(questions)
    
    # Если нашли несколько вопросов, считаем текст FAQ
    return question_count >= 2

def find_request_response_pairs(text: str) -> List[Dict[str, str]]:
    """
    Находит пары запрос-ответ API в тексте.
    
    Args:
        text: Текст для анализа
        
    Returns:
        Список словарей с запросами и ответами
    """
    pairs = []
    
    # Ищем пары "запрос-ответ" по типичной структуре документации API
    request_patterns = [
        r'(?:Пример запроса|Параметры запроса|Request)[\s\S]+?```[\s\S]+?```',
        r'(?:POST|GET|PUT|DELETE|PATCH)[\s\S]+?```[\s\S]+?```'
    ]
    
    response_patterns = [
        r'(?:Пример ответа|Параметры ответа|Response)[\s\S]+?```[\s\S]+?```',
        r'HTTP/\d\.\d \d{3}[\s\S]+?```[\s\S]+?```'
    ]
    
    # Ищем запросы
    requests = []
    for pattern in request_patterns:
        found = re.findall(pattern, text)
        requests.extend(found)
    
    # Ищем ответы
    responses = []
    for pattern in response_patterns:
        found = re.findall(pattern, text)
        responses.extend(found)
    
    # Сопоставляем запросы и ответы, если они следуют один за другим
    for i, req in enumerate(requests):
        req_end = text.find(req) + len(req)
        
        # Ищем ответ, который идет сразу после запроса
        closest_resp = None
        closest_dist = float('inf')
        
        for resp in responses:
            resp_start = text.find(resp)
            if resp_start > req_end:  # Ответ идет после запроса
                dist = resp_start - req_end
                if dist < closest_dist:
                    closest_dist = dist
                    closest_resp = resp
        
        # Если нашли близкий ответ, создаем пару
        if closest_resp and closest_dist < 500:  # Эвристически определяем, что ответ связан с запросом
            pairs.append({
                "request": req,
                "response": closest_resp
            })
    
    return pairs

def process_support_documentation(
    text: str, 
    metadata: Dict[str, Any],
    chunk_size: int = 1200,  # Увеличено с 800
    chunk_overlap: int = 150  # Увеличено со 100
) -> List[Dict[str, Any]]:
    """
    Специализированная обработка для документации поддержки.
    
    Args:
        text: Текст для обработки
        metadata: Дополнительные метаданные
        chunk_size: Целевой размер чанка
        chunk_overlap: Перекрытие между чанками
        
    Returns:
        Список словарей с чанками
    """
    chunks = []
    
    # Определяем структуру контента
    is_step_by_step = is_step_by_step_content(text)
    is_faq = is_faq_content(text)
    
    doc_type = "tutorial" if is_step_by_step else "faq" if is_faq else "support"
    
    # Добавляем контекстный префикс и обновляем метаданные
    context_prefix, additional_metadata = create_metadata_prefixes(doc_type, metadata)
    updated_metadata = {**metadata, **additional_metadata}
    
    # Ищем блоки кода для сохранения их целостности
    code_blocks = process_code_blocks(text)
    
    # Создаем копию текста для маркировки
    marked_text = text
    
    # Заменяем блоки кода маркерами
    for block in code_blocks:
        marked_text = marked_text[:block["start"]] + f"[[CODE_BLOCK_{block['id']}]]" + marked_text[block["end"]:]
    
    # Определяем стратегию разбиения в зависимости от типа контента
    if is_step_by_step:
        # Для пошаговых инструкций используем специальную логику для сохранения шагов вместе
        
        # Выделяем шаги как отдельные смысловые блоки
        step_pattern = r'(?:\d+\.\s+[^\n]+|\bШаг\s+\d+:[^\n]+)(?:\n(?!\d+\.|Шаг\s+\d+:)[^\n]+)*'
        steps = re.findall(step_pattern, marked_text, re.DOTALL)
        
        if steps:
            # Группируем последовательные шаги в один чанк
            step_groups = []
            current_group = []
            total_words = 0
            
            for step in steps:
                step_words = len(step.split())
                
                # Если добавление шага не превысит размер чанка, добавляем его к группе
                # Увеличиваем допустимый размер группы для лучшего RAG
                if total_words + step_words <= chunk_size * 1.5:  # Было 1.5
                    current_group.append(step)
                    total_words += step_words
                else:
                    # Если группа не пуста, завершаем ее
                    if current_group:
                        step_groups.append(current_group)
                    # Начинаем новую группу с текущим шагом
                    current_group = [step]
                    total_words = step_words
            
            # Добавляем последнюю группу, если она не пуста
            if current_group:
                step_groups.append(current_group)
            
            # Создаем чанки из групп шагов
            for group in step_groups:
                # Соединяем шаги в группе
                group_text = "\n\n".join(group)
                
                # Восстанавливаем код в группе
                for block in code_blocks:
                    if f"[[CODE_BLOCK_{block['id']}]]" in group_text:
                        code_block = f"```{block['lang']}\n{block['code']}\n```"
                        group_text = group_text.replace(f"[[CODE_BLOCK_{block['id']}]]", code_block)
                
                # Применяем обработку текста
                processed_text = fix_url_paths(group_text)
                processed_text = normalize_phone_number(processed_text)
                processed_text = cleanup_markdown_artifacts(processed_text)
                
                # Увеличиваем минимальный порог размера чанка
                if len(processed_text.split()) >= 60:  # Было 40
                    # Извлекаем ключевые термины для метаданных
                    key_terms = extract_key_terms(processed_text, doc_type)
                    chunk_metadata = updated_metadata.copy()
                    if key_terms:
                        chunk_metadata["key_terms"] = key_terms
                    
                    # Указываем в метаданных, что это пошаговая инструкция
                    chunk_metadata["content_type"] = "step_by_step"
                    
                    chunks.append({
                        "text": context_prefix + processed_text,
                        "metadata": chunk_metadata
                    })
            
            # Обрабатываем оставшийся текст
            remaining_text = marked_text
            for step in steps:
                remaining_text = remaining_text.replace(step, "")
            
            if len(remaining_text.strip()) > 0:
                # Разбиваем оставшийся текст стандартным способом с увеличенным размером чанка
                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap,
                    separators=["\n## ", "\n### ", "\n\n", "\n", ". ", "! ", "? "],
                    keep_separator=True
                )
                remaining_splits = splitter.split_text(remaining_text)
                
                for split in remaining_splits:
                    # Восстанавливаем код
                    restored_split = split
                    for block in code_blocks:
                        if f"[[CODE_BLOCK_{block['id']}]]" in restored_split:
                            code_block = f"```{block['lang']}\n{block['code']}\n```"
                            restored_split = restored_split.replace(f"[[CODE_BLOCK_{block['id']}]]", code_block)
                    
                    # Применяем обработку текста
                    processed_split = fix_url_paths(restored_split)
                    processed_split = normalize_phone_number(processed_split)
                    processed_split = cleanup_markdown_artifacts(processed_split)
                    
                    # Увеличиваем минимальный порог размера чанка
                    if len(processed_split.split()) >= 60:  # Было 40
                        key_terms = extract_key_terms(processed_split, doc_type)
                        chunk_metadata = updated_metadata.copy()
                        if key_terms:
                            chunk_metadata["key_terms"] = key_terms
                        
                        chunks.append({
                            "text": context_prefix + processed_split,
                            "metadata": chunk_metadata
                        })
            
            return chunks
    
    elif is_faq:
        # Для FAQ ищем пары вопрос-ответ и сохраняем их вместе
        faq_pattern = r'(?:Как|Почему|Где|Когда|Что такое|Зачем)[^\.]+\?\s*(?:\n|.)+?(?=(?:Как|Почему|Где|Когда|Что такое|Зачем)[^\.]+\?|$)'
        qa_pairs = re.findall(faq_pattern, marked_text, re.DOTALL)
        
        if qa_pairs:
            for qa in qa_pairs:
                # Восстанавливаем код в вопросе-ответе
                restored_qa = qa
                for block in code_blocks:
                    if f"[[CODE_BLOCK_{block['id']}]]" in restored_qa:
                        code_block = f"```{block['lang']}\n{block['code']}\n```"
                        restored_qa = restored_qa.replace(f"[[CODE_BLOCK_{block['id']}]]", code_block)
                
                # Для длинных пар вопрос-ответ делаем специальную обработку
                # Увеличиваем порог для определения длинного Q&A
                if len(restored_qa.split()) > chunk_size * 1.3:  # Было просто chunk_size
                    # Находим вопрос (первое предложение, заканчивающееся вопросительным знаком)
                    question_match = re.search(r'^.*?\?', restored_qa)
                    if question_match:
                        question = question_match.group(0)
                        answer = restored_qa[len(question):].strip()
                        
                        # Разбиваем только ответ на фрагменты
                        answer_splitter = RecursiveCharacterTextSplitter(
                            chunk_size=chunk_size - len(question.split()),
                            chunk_overlap=chunk_overlap,
                            separators=["\n\n", "\n", ". ", "! ", "? "],
                            keep_separator=True
                        )
                        answer_chunks = answer_splitter.split_text(answer)
                        
                        # Первый чанк содержит вопрос и начало ответа
                        processed_first = fix_url_paths(question + "\n\n" + answer_chunks[0])
                        processed_first = normalize_phone_number(processed_first)
                        processed_first = cleanup_markdown_artifacts(processed_first)
                        
                        # Добавляем чанк
                        key_terms = extract_key_terms(processed_first, "faq")
                        chunk_metadata = updated_metadata.copy()
                        if key_terms:
                            chunk_metadata["key_terms"] = key_terms
                        
                        chunk_metadata["faq_part"] = "question_with_partial_answer"
                        
                        chunks.append({
                            "text": context_prefix + processed_first,
                            "metadata": chunk_metadata
                        })
                        
                        # Остальные чанки содержат продолжение ответа
                        for i, answer_chunk in enumerate(answer_chunks[1:], 1):
                            processed_chunk = fix_url_paths(answer_chunk)
                            processed_chunk = normalize_phone_number(processed_chunk)
                            processed_chunk = cleanup_markdown_artifacts(processed_chunk)
                            
                            key_terms = extract_key_terms(processed_chunk, "faq")
                            chunk_metadata = updated_metadata.copy()
                            if key_terms:
                                chunk_metadata["key_terms"] = key_terms
                            
                            chunk_metadata["faq_part"] = "answer_continuation"
                            chunk_metadata["question_ref"] = question[:50] + "..." if len(question) > 50 else question
                            
                            chunks.append({
                                "text": context_prefix + "Продолжение ответа на вопрос: " + question + "\n\n" + processed_chunk,
                                "metadata": chunk_metadata
                            })
                else:
                    # Для коротких пар вопрос-ответ сохраняем их вместе
                    processed_qa = fix_url_paths(restored_qa)
                    processed_qa = normalize_phone_number(processed_qa)
                    processed_qa = cleanup_markdown_artifacts(processed_qa)
                    
                    key_terms = extract_key_terms(processed_qa, "faq")
                    chunk_metadata = updated_metadata.copy()
                    if key_terms:
                        chunk_metadata["key_terms"] = key_terms
                    
                    chunk_metadata["content_type"] = "faq_qa_pair"
                    
                    chunks.append({
                        "text": context_prefix + processed_qa,
                        "metadata": chunk_metadata
                    })
            
            # Обрабатываем оставшийся текст
            remaining_text = marked_text
            for qa in qa_pairs:
                remaining_text = remaining_text.replace(qa, "")
            
            if len(remaining_text.strip()) > 0:
                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap,
                    separators=["\n## ", "\n### ", "\n\n", "\n", ". ", "! ", "? "],
                    keep_separator=True
                )
                remaining_splits = splitter.split_text(remaining_text)
                
                for split in remaining_splits:
                    # Восстанавливаем код
                    restored_split = split
                    for block in code_blocks:
                        if f"[[CODE_BLOCK_{block['id']}]]" in restored_split:
                            code_block = f"```{block['lang']}\n{block['code']}\n```"
                            restored_split = restored_split.replace(f"[[CODE_BLOCK_{block['id']}]]", code_block)
                    
                    # Применяем обработку текста
                    processed_split = fix_url_paths(restored_split)
                    processed_split = normalize_phone_number(processed_split)
                    processed_split = cleanup_markdown_artifacts(processed_split)
                    
                    # Увеличиваем минимальный порог размера чанка
                    if len(processed_split.split()) >= 60:  # Было 40
                        key_terms = extract_key_terms(processed_split, doc_type)
                        chunk_metadata = updated_metadata.copy()
                        if key_terms:
                            chunk_metadata["key_terms"] = key_terms
                        
                        chunks.append({
                            "text": context_prefix + processed_split,
                            "metadata": chunk_metadata
                        })
            
            return chunks
    
    # Если не применились специальные стратегии или для обычной документации
    # используем стандартную обработку с увеличенным размером чанка
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n## ", "\n### ", "\n\n", "\n", ". ", "! ", "? "],
        keep_separator=True
    )
    splits = splitter.split_text(marked_text)
    
    for split in splits:
        # Восстанавливаем код
        restored_split = split
        for block in code_blocks:
            if f"[[CODE_BLOCK_{block['id']}]]" in restored_split:
                code_block = f"```{block['lang']}\n{block['code']}\n```"
                restored_split = restored_split.replace(f"[[CODE_BLOCK_{block['id']}]]", code_block)
        
        # Применяем обработку текста
        processed_split = fix_url_paths(restored_split)
        processed_split = normalize_phone_number(processed_split)
        processed_split = cleanup_markdown_artifacts(processed_split)
        processed_split = fix_code_blocks(processed_split)
        
        # Увеличиваем минимальный порог размера чанка
        if len(processed_split.split()) >= 60:  # Было 40
            key_terms = extract_key_terms(processed_split, doc_type)
            chunk_metadata = updated_metadata.copy()
            if key_terms:
                chunk_metadata["key_terms"] = key_terms
            
            chunks.append({
                "text": context_prefix + processed_split,
                "metadata": chunk_metadata
            })
    
    return chunks

def create_chunks_from_markdown(
    markdown_text: str, 
    source_path: str, 
    url: str,
    title: str,
    section: str,
    chunk_size: int = 1200,  # Увеличено с 800
    chunk_overlap: int = 150  # Увеличено со 100
) -> List[Dict[str, Any]]:
    """
    Создает семантически значимые чанки из markdown текста с иерархической структурой.
    
    Args:
        markdown_text: Текст в формате Markdown
        source_path: Путь к исходному файлу
        url: URL исходной страницы
        title: Заголовок страницы
        section: Раздел (например, developers, support)
        chunk_size: Целевой размер чанка в токенах
        chunk_overlap: Перекрытие между чанками в токенах
    
    Returns:
        Список словарей с полями text и metadata
    """
    # Удаляем YAML frontmatter из начала файла если он есть
    markdown_text = re.sub(r'^---\n.*?\n---\n', '', markdown_text, flags=re.DOTALL)
    
    # Исправляем проблемы с форматированием кода
    markdown_text = fix_code_blocks(markdown_text)
    
    # Определяем тип документации
    doc_type = detect_document_type(source_path, markdown_text)
    
    # Определяем специальные структуры в тексте
    has_api_examples = bool(re.search(r'(GET|POST|PUT|DELETE|PATCH)\s+[^\s]+', markdown_text))
    has_request_response = bool(re.search(r'(Пример запроса|Пример ответа|Request|Response)', markdown_text))
    has_steps = is_step_by_step_content(markdown_text)
    has_faq = is_faq_content(markdown_text)
    
    # Адаптивное определение размера чанка на основе типа контента
    # ОПТИМИЗИРОВАНО ДЛЯ RAG - значительно увеличиваем размеры чанков
    adaptive_chunk_size = chunk_size
    adaptive_chunk_overlap = chunk_overlap
    
    if doc_type == "api" and (has_api_examples or has_request_response):
        adaptive_chunk_size = int(chunk_size * 1.5)  # Было 1.3
        adaptive_chunk_overlap = int(chunk_overlap * 1.5)  # Было 1.3
    elif has_steps:
        adaptive_chunk_size = int(chunk_size * 1.4)  # Было 1.2
        adaptive_chunk_overlap = int(chunk_overlap * 1.4)  # Было 1.2
    elif has_faq:
        adaptive_chunk_size = int(chunk_size * 1.3)  # Было 1.1
        adaptive_chunk_overlap = int(chunk_overlap * 1.3)  # Было 1.1
    
    # Определяем стратегию разделения по заголовкам
    # Для оптимальных RAG-чанков предпочитаем разделять по более крупным заголовкам
    headers_to_split_on = HEADERS_TO_SPLIT_ON
    
    # Для небольших документов можем вообще не разделять по мелким заголовкам
    if len(markdown_text.split()) < 1500:  # для небольших документов
        # Убираем разделение по мелким заголовкам (h4-h6)
        headers_to_split_on = HEADERS_TO_SPLIT_ON[:3]
    
    # Сначала разделяем по заголовкам
    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on
    )
    header_splits = markdown_splitter.split_text(markdown_text)
    
    # Финальный список чанков
    final_chunks = []
    
    # Извлекаем версию API если она указана в документе
    api_version = None
    if doc_type == "api":
        version_match = re.search(r'(v\d+(\.\d+)?|версия\s+\d+(\.\d+)?)', markdown_text, re.IGNORECASE)
        if version_match:
            api_version = version_match.group(0)
    
    # Обрабатываем каждый фрагмент, разделенный по заголовкам
    for i, doc in enumerate(header_splits):
        print(f"\nProcessing header split {i+1}...")
        # --- НАЧАЛО ИЗМЕНЕНИЙ v2 ---
        # 1. Формируем section_headers и очищаем исходные метаданные от header_X
        section_headers = []
        original_doc_metadata = doc.metadata.copy() if doc.metadata else {}
        print(f"  Original doc.metadata: {original_doc_metadata}")
        headers_to_remove = []
        for h_level in range(1, 7):
            header_key = f"header_{h_level}"
            if header_key in original_doc_metadata and original_doc_metadata[header_key]:
                section_headers.append(original_doc_metadata[header_key])
                headers_to_remove.append(header_key)
            # Удаляем ключ из копии, чтобы он не попал в final_metadata случайно
            original_doc_metadata.pop(header_key, None)

        print(f"  Generated section_headers: {section_headers}")

        # 2. Создаем финальный словарь метаданных для этого раздела документа
        # Начинаем с базовых данных файла
        final_metadata_for_section = {
            "source": source_path,
            "url": url,
            "title": title,
            "section": section,
            "doc_type": doc_type, # Тип документа определен ранее
            "section_headers": section_headers # Добавляем собранные заголовки
        }
        # Добавляем версию API, если есть
        if api_version:
            final_metadata_for_section["api_version"] = api_version
        # Можно добавить оставшиеся метаданные от сплиттера (если есть и нужны)
        # final_metadata_for_section.update(original_doc_metadata)

        print(f"  Final metadata for section: {final_metadata_for_section}")
        # --- КОНЕЦ ИЗМЕНЕНИЙ v2 ---

        # Текст документа (этой секции)
        text = doc.page_content
        text = text.strip()

        if not text:
            print(f"  Skipping empty text section.")
            continue

        # Обрабатываем по-разному в зависимости от типа документации
        # Передаем ТОЛЬКО СОЗДАННЫЙ СЛОВАРЬ final_metadata_for_section
        if doc_type == "api":
            section_chunks = process_api_documentation(
                text, final_metadata_for_section, adaptive_chunk_size, adaptive_chunk_overlap
            )
        else:  # support, faq или tutorial
            section_chunks = process_support_documentation(
                text, final_metadata_for_section, adaptive_chunk_size, adaptive_chunk_overlap
            )

        print(f"  Generated {len(section_chunks)} chunks from this section.")
        final_chunks.extend(section_chunks)

    return final_chunks

def get_chunk_hash(chunk_text: str) -> str:
    """
    Создает хеш текста чанка для дедупликации.
    
    Args:
        chunk_text: Текст чанка
        
    Returns:
        Строка с хешем текста
    """
    # Предобработка: приводим к нижнему регистру, удаляем лишние пробелы
    normalized_text = re.sub(r'\s+', ' ', chunk_text.lower().strip())
    # Удаляем префиксы типа "API Метод:", которые могут создавать ложные отличия
    normalized_text = re.sub(r'^(api метод:|метод возвращает:|метод принимает:)', '', normalized_text)
    # Создаем хеш
    return hashlib.md5(normalized_text.encode('utf-8')).hexdigest()

def check_chunks_similarity(chunk1: str, chunk2: str) -> float:
    """
    Проверяет, насколько похожи два чанка текста.
    
    Args:
        chunk1: Первый чанк текста
        chunk2: Второй чанк текста
        
    Returns:
        Значение от 0 до 1, где 1 означает полную идентичность, а 0 - полное различие
    """
    # Нормализуем тексты
    text1 = re.sub(r'\s+', ' ', chunk1.lower().strip())
    text2 = re.sub(r'\s+', ' ', chunk2.lower().strip())
    
    # Удаляем общие префиксы
    text1 = re.sub(r'^(api метод:|метод возвращает:|метод принимает:)', '', text1)
    text2 = re.sub(r'^(api метод:|метод возвращает:|метод принимает:)', '', text2)
    
    # Разбиваем на слова
    words1 = set(text1.split())
    words2 = set(text2.split())
    
    # Подсчитываем общие слова
    common_words = len(words1.intersection(words2))
    
    # Подсчитываем Жаккардово сходство: |A ∩ B| / |A ∪ B|
    total_unique_words = len(words1.union(words2))
    if total_unique_words == 0:
        return 0.0
    
    return common_words / total_unique_words

def deduplicate_chunks(chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Удаляет дубликаты и очень похожие чанки, оставляя только уникальные тексты.
    
    Args:
        chunks: Список словарей с чанками
        
    Returns:
        Список уникальных чанков
    """
    unique_chunks = []
    seen_hashes = set()
    duplicates_count = 0
    similar_count = 0
    
    # Сортируем чанки по длине (предпочитаем более информативные)
    sorted_chunks = sorted(chunks, key=lambda c: len(c["text"].split()), reverse=True)
    total_chunks_to_process = len(sorted_chunks)
    print(f"\nStarting deduplication process for {total_chunks_to_process} chunks...") # Отладка

    for chunk_index, chunk in enumerate(sorted_chunks):
        # Получаем хеш текста чанка
        chunk_hash = get_chunk_hash(chunk["text"])

        # Если этот хеш мы еще не видели, проверяем на похожесть
        if chunk_hash not in seen_hashes:
            is_similar = False
            # Отладка: Начало проверки на похожесть
            print(f"  [{chunk_index+1}/{total_chunks_to_process}] Checking chunk (hash: {chunk_hash[:8]}...) for similarity against {len(unique_chunks)} unique chunks...")
            start_similarity_check_time = time.time() # Отладка времени

            for existing_chunk_index, existing_chunk in enumerate(unique_chunks):
                # Можно раскомментировать для ОЧЕНЬ детальной отладки, но будет много вывода
                # print(f"    Comparing with existing chunk {existing_chunk_index+1}")
                similarity = check_chunks_similarity(chunk["text"], existing_chunk["text"])
                # Если похожесть высокая, считаем чанк похожим
                if similarity > 0.7:  # Порог похожести 70%
                    print(f"    -> Found similar chunk (similarity: {similarity:.2f})! Skipping.")
                    is_similar = True
                    similar_count += 1
                    break # Выходим из внутреннего цикла, если нашли похожесть

            # Отладка: Конец проверки на похожесть
            similarity_check_duration = time.time() - start_similarity_check_time
            print(f"  Similarity check took {similarity_check_duration:.2f} seconds.")

            if not is_similar:
                print(f"  Chunk {chunk_index+1} is unique. Adding.")
                seen_hashes.add(chunk_hash)
                unique_chunks.append(chunk)
            # else: # Уже вывели сообщение "Found similar..."
            #     pass
        else:
            # Можно раскомментировать для отладки дубликатов по хешу
            # print(f"  [{chunk_index+1}/{total_chunks_to_process}] Duplicate hash found. Skipping.")
            duplicates_count += 1

    print(f"\nУдалено дубликатов по хешу: {duplicates_count}") # Обновил текст
    print(f"Удалено похожих чанков (сходство > 0.7): {similar_count}") # Обновил текст
    return unique_chunks

def extract_key_terms(text: str, doc_type: str = "general") -> List[str]:
    """
    Извлекает ключевые термины из текста для улучшения поиска.
    Оптимизированная версия с фокусом на бизнес-сущности и технические термины.
    
    Args:
        text: Текст для анализа
        doc_type: Тип документа ("api", "support", "faq", "tutorial", "general")
        
    Returns:
        Список ключевых терминов
    """
    key_terms = []
    
    # Определяем бизнес-сущности amoCRM в тексте
    for entity_type, entity_words in ENTITY_TYPES.items():
        for word in entity_words:
            if re.search(r'\b' + word + r'\b', text.lower()):
                if entity_type not in key_terms:
                    key_terms.append(entity_type)
    
    # Для API документации добавляем специфичные элементы
    if doc_type == "api":
        # Извлекаем методы API (GET, POST и т.д.)
        for pattern in API_METHOD_PATTERNS:
            matches = re.findall(pattern, text)
            for match in matches:
                if len(match) >= 2:
                    method_term = f"{match[0]} {match[1].strip()}"
                    if len(method_term) > 5 and method_term not in key_terms:
                        key_terms.append(method_term)
        
        # Извлекаем параметры API (только значимые)
        api_params = re.findall(r'\|\s*([a-zA-Z0-9_\-]+)\s*\|', text)
        for param in api_params:
            # Фильтруем общие слова и типы данных
            if len(param) > 3 and param.lower() not in ['int', 'string', 'bool', 'array', 'object', 'type', 'id', 'name', 'description', 'null']:
                key_terms.append(param)
        
        # Извлекаем имена полей из JSON-примеров
        json_fields = re.findall(r'"([a-zA-Z0-9_]+)":', text)
        for field in json_fields:
            if len(field) > 3 and field.lower() not in ['id', 'name', 'type', 'value', 'status', 'data', 'result', 'error', 'success', 'code']:
                key_terms.append(field)
    
    # Для FAQ и поддержки извлекаем клиентские термины
    elif doc_type in ["faq", "support", "tutorial"]:
        # Извлекаем имена функций или интерфейсных элементов (выделенные в кавычки или апострофы)
        ui_elements = re.findall(r'[«"\']([а-яА-Яa-zA-Z0-9_\s\-]+)[»"\']', text)
        for element in ui_elements:
            if 3 < len(element) < 30 and element not in key_terms:
                key_terms.append(element)
    
    # Удаляем префиксы/суффиксы типа _embedded, []
    clean_terms = []
    for term in key_terms:
        # Удаляем технические префиксы
        term = re.sub(r'^(_embedded|_links)', '', term)
        # Удаляем индексы массивов
        term = re.sub(r'\[\d+\]', '', term)
        # Удаляем символы [] и пустые строки
        term = term.replace('[', '').replace(']', '').strip()
        if term and term not in clean_terms:
            clean_terms.append(term)
    
    # Ограничиваем количество ключевых терминов
    return list(set(clean_terms))[:10]  # Не более 10 ключевых терминов

def process_all_markdown_files(markdown_dir: str, output_jsonl: str) -> None:
    """
    Обрабатывает все Markdown файлы в указанной директории и создает файл с чанками
    
    Args:
        markdown_dir: Путь к директории с Markdown файлами
        output_jsonl: Путь к выходному JSONL файлу с чанками
    """
    # Получаем список файлов
    markdown_files = glob.glob(os.path.join(markdown_dir, "**/*.md"), recursive=True)
    
    # Создаем директорию для выходного файла, если она не существует
    output_dir = os.path.dirname(output_jsonl)
    os.makedirs(output_dir, exist_ok=True)
    
    # Обрабатываем каждый файл
    all_chunks = []
    for file_path in markdown_files:
        try:
            rel_path = os.path.relpath(file_path, os.path.dirname(markdown_dir))
            
            # Извлекаем информацию из пути файла
            parts = Path(rel_path).parts
            section = parts[0] if len(parts) > 0 else "unknown"
            
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Извлекаем метаданные из frontmatter
            url = ""
            title = ""
            frontmatter_match = re.search(r'^---\n(.*?)\n---\n', content, re.DOTALL)
            if frontmatter_match:
                frontmatter = frontmatter_match.group(1)
                url_match = re.search(r'url:\s*(.*)', frontmatter)
                title_match = re.search(r'title:\s*"(.*?)"', frontmatter)
                
                if url_match:
                    url = url_match.group(1).strip()
                if title_match:
                    title = title_match.group(1).strip()
            
            # Если заголовок не найден, используем имя файла или извлекаем из первого заголовка
            if not title:
                # Попытка найти заголовок в тексте
                title_match = re.search(r'^#\s+(.*?)$', content, re.MULTILINE)
                if title_match:
                    title = title_match.group(1).strip()
                else:
                    title = os.path.splitext(os.path.basename(file_path))[0]
            
            # Определяем тип документа для адаптивной настройки размера чанка
            doc_type = detect_document_type(file_path, content)
            
            # Адаптивная настройка размера чанка на основе типа документа и размера контента
            # ИЗМЕНЕНО: УМЕНЬШАЕМ РАЗМЕРЫ ЧАНКОВ ДЛЯ ЛУЧШЕГО БАЛАНСА
            if doc_type == "api":
                # Для API документации размер чанка для сохранения контекста
                chunk_size = 1200  # Было 1500
                chunk_overlap = 200
            elif doc_type == "tutorial":
                # Для пошаговых инструкций размер для сохранения шагов вместе
                chunk_size = 1100  # Было 1400
                chunk_overlap = 180
            elif doc_type == "faq":
                # Для FAQ оптимизируем для пар вопрос-ответ
                chunk_size = 1000  # Было 1300
                chunk_overlap = 150
            else:
                # Стандартный размер для общей документации
                chunk_size = 900  # Было 1200
                chunk_overlap = 120
            
            # Создаем чанки
            chunks = create_chunks_from_markdown(
                content, file_path, url, title, section, 
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )
            
            all_chunks.extend(chunks)
            print(f"Обработан файл: {file_path}, создано чанков: {len(chunks)}")
            
        except Exception as e:
            print(f"Ошибка при обработке файла {file_path}: {str(e)}")
    
    # Применяем улучшенную дедупликацию чанков
    print(f"Всего создано чанков до дедупликации: {len(all_chunks)}")
    
    # ОБЪЕДИНЯЕМ КОРОТКИЕ ЧАНКИ И РАЗБИВАЕМ СЛИШКОМ БОЛЬШИЕ
    all_chunks = merge_short_chunks(all_chunks)
    print(f"Чанков после объединения коротких и разбивки больших: {len(all_chunks)}")
    
    # Добавляем постобработку для ограничения размера чанков
    all_chunks = post_process_chunk_sizes(all_chunks)
    print(f"Чанков после постобработки размеров: {len(all_chunks)}")
    
    unique_chunks = deduplicate_chunks(all_chunks)
    print(f"Чанков после дедупликации: {len(unique_chunks)}")
    
    # Добавляем теги бизнес-сущностей к каждому чанку
    for chunk in unique_chunks:
        # Идентифицируем бизнес-сущности в тексте
        entities = []
        for entity_type, entity_words in ENTITY_TYPES.items():
            for word in entity_words:
                if re.search(r'\b' + word + r'\b', chunk["text"].lower()):
                    if entity_type not in entities:
                        entities.append(entity_type)
        
        # Если найдены сущности, добавляем их в метаданные
        if entities:
            chunk["metadata"]["entities"] = entities
        
        # Извлекаем ключевые термины, если не добавлены ранее
        if "key_terms" not in chunk["metadata"]:
            doc_type = chunk["metadata"].get("doc_type", "general")
            key_terms = extract_key_terms(chunk["text"], doc_type)
            if key_terms:
                chunk["metadata"]["key_terms"] = key_terms
    
    # Записываем уникальные чанки в JSONL файл
    with open(output_jsonl, 'w', encoding='utf-8') as f:
        for chunk in unique_chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + '\n')
    
    print(f"Обработка завершена. Всего создано уникальных чанков: {len(unique_chunks)}")
    print(f"Результат сохранен в: {output_jsonl}")

def merge_short_chunks(chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Объединяет короткие чанки с похожими метаданными для создания более оптимальных чанков для RAG.
    
    Args:
        chunks: Список словарей с чанками
        
    Returns:
        Список оптимизированных чанков с объединенными короткими чанками
    """
    # Сначала сортируем чанки по источнику и заголовкам
    chunks.sort(key=lambda c: (
        c["metadata"].get("source", ""),
        c["metadata"].get("title", ""),
        c["metadata"].get("header_1", ""),
        c["metadata"].get("header_2", ""),
        c["metadata"].get("header_3", "")
    ))
    
    merged_chunks = []
    i = 0
    
    while i < len(chunks):
        current_chunk = chunks[i]
        current_text = current_chunk["text"]
        current_words = len(current_text.split())
        current_char_count = len(current_text)
        
        # ДОБАВЛЕНО: Если текущий чанк уже слишком большой, разбиваем его на части
        if current_words > 800 or current_char_count > 6000:  # ~1000 токенов
            sub_chunks = split_large_chunk(current_chunk)
            merged_chunks.extend(sub_chunks)
            i += 1
            continue
        
        # Если текущий чанк короткий (менее 150 слов), проверяем следующий
        if current_words < 150 and i + 1 < len(chunks):
            next_chunk = chunks[i + 1]
            next_words = len(next_chunk["text"].split())
            combined_words = current_words + next_words
            combined_chars = current_char_count + len(next_chunk["text"])
            
            # Проверяем, схожи ли метаданные (тот же источник и похожие заголовки)
            same_source = current_chunk["metadata"].get("source") == next_chunk["metadata"].get("source")
            same_title = current_chunk["metadata"].get("title") == next_chunk["metadata"].get("title")
            same_doc_type = current_chunk["metadata"].get("doc_type") == next_chunk["metadata"].get("doc_type")
            
            # ИЗМЕНЕНО: Добавлена проверка максимального размера объединенного чанка
            # Если метаданные похожи и общий размер подходит для RAG (не слишком большой)
            if same_source and same_title and same_doc_type and combined_words <= 500 and combined_chars <= 4000:
                # Объединяем чанки
                merged_text = current_text + "\n\n" + next_chunk["text"]
                
                # Объединяем ключевые термины, если они есть
                merged_metadata = current_chunk["metadata"].copy()
                
                if "key_terms" in current_chunk["metadata"] and "key_terms" in next_chunk["metadata"]:
                    merged_key_terms = list(set(current_chunk["metadata"]["key_terms"] + next_chunk["metadata"]["key_terms"]))
                    merged_metadata["key_terms"] = merged_key_terms[:10]  # Не более 10 ключевых терминов
                
                # Объединяем entities, если они есть
                if "entities" in current_chunk["metadata"] and "entities" in next_chunk["metadata"]:
                    merged_entities = list(set(current_chunk["metadata"].get("entities", []) + next_chunk["metadata"].get("entities", [])))
                    merged_metadata["entities"] = merged_entities
                
                merged_chunks.append({
                    "text": merged_text,
                    "metadata": merged_metadata
                })
                
                # Пропускаем следующий чанк, так как мы его объединили с текущим
                i += 2
                continue
        
        # Если не объединяли, добавляем текущий чанк как есть
        merged_chunks.append(current_chunk)
        i += 1
    
    return merged_chunks

def split_large_chunk(chunk: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Разбивает слишком большой чанк на несколько меньших чанков.
    
    Args:
        chunk: Словарь с чанком, который нужно разбить
        
    Returns:
        Список меньших чанков
    """
    text = chunk["text"]
    metadata = chunk["metadata"]
    
    # Определяем оптимальный способ разбиения в зависимости от типа документа
    doc_type = metadata.get("doc_type", "general")
    
    # Создаем сплиттер с настройками для разбивки больших чанков
    # Уменьшаем размер чанка до ~700 слов (~800-900 токенов)
    # и увеличиваем перекрытие для лучшей связности
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=5500,  # ~800-900 токенов
        chunk_overlap=800,  # ~100-120 токенов
        separators=["\n## ", "\n### ", "\n#### ", "\n\n", "\n", ". ", "! ", "? ", ";", ":", " ", ""],
        keep_separator=True
    )
    
    # Разбиваем текст на части
    text_splits = splitter.split_text(text)
    
    # Создаем новые чанки с теми же метаданными
    smaller_chunks = []
    for split_text in text_splits:
        # Проверяем минимальный размер чанка
        if len(split_text.split()) < 60:
            continue
            
        smaller_chunks.append({
            "text": split_text,
            "metadata": metadata.copy()
        })
    
    return smaller_chunks

def post_process_chunk_sizes(chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Дополнительная обработка для контроля размера чанков.
    Разбивает слишком большие чанки на более мелкие.
    
    Args:
        chunks: Список словарей с чанками
        
    Returns:
        Список чанков с контролируемыми размерами
    """
    processed_chunks = []
    large_chunks_count = 0
    
    for chunk in chunks:
        text = chunk["text"]
        word_count = len(text.split())
        char_count = len(text)
        
        # Если чанк превышает максимально допустимый размер (~1000-1200 токенов)
        if word_count > 800 or char_count > 6000:
            large_chunks_count += 1
            sub_chunks = split_large_chunk(chunk)
            processed_chunks.extend(sub_chunks)
        else:
            processed_chunks.append(chunk)
    
    print(f"Обнаружено и разбито крупных чанков: {large_chunks_count}")
    return processed_chunks

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Создание чанков из Markdown файлов")
    parser.add_argument("--input_dir", type=str, default="database/processed_markdown",
                        help="Директория с Markdown файлами")
    parser.add_argument("--output_file", type=str, default="database/chunks/chunks.jsonl",
                        help="Путь к выходному JSONL файлу")
    parser.add_argument("--chunk_size", type=int, default=800,
                        help="Целевой размер чанка в токенах")
    parser.add_argument("--chunk_overlap", type=int, default=100,
                        help="Перекрытие между чанками в токенах")
    
    args = parser.parse_args()
    
    # Обработка всех файлов с заданными параметрами
    process_all_markdown_files(args.input_dir, args.output_file) 