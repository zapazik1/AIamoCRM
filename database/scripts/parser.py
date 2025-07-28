import os
import re
import glob
import logging
from bs4 import BeautifulSoup, Comment
from markdownify import markdownify as md
from urllib.parse import urlparse, unquote
from tqdm import tqdm

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join('database', 'parser.log'), encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Пути для исходных HTML-файлов и результирующих Markdown-файлов
HTML_SUPPORT_PATH = os.path.join('database', 'raw_html', 'support')
HTML_DEV_PATH = os.path.join('database', 'raw_html', 'developers')
MARKDOWN_PATH = os.path.join('database', 'processed_markdown')

# Создание директории для Markdown, если она не существует
os.makedirs(MARKDOWN_PATH, exist_ok=True)
os.makedirs(os.path.join(MARKDOWN_PATH, 'support'), exist_ok=True)
os.makedirs(os.path.join(MARKDOWN_PATH, 'developers'), exist_ok=True)

# Шаблоны имен файлов, которые следует пропустить (бинарные файлы, архивы и пр.)
SKIP_FILE_PATTERNS = [
    r'\.zip\.html$',
    r'\.csv\.html$',
    r'\.pdf\.html$',
    r'\.doc\.html$',
    r'\.xls\.html$',
    r'static_assets.*\.(zip|csv|pdf|doc|xls)'
]

def should_skip_file(filename):
    """Проверка, следует ли пропустить файл на основе его имени"""
    for pattern in SKIP_FILE_PATTERNS:
        if re.search(pattern, filename, re.IGNORECASE):
            return True
    return False

def clean_html(html_content):
    """Предварительная очистка HTML для улучшения преобразования в Markdown"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Удаление ненужных элементов (навигация, футер, скрипты, стили и т.д.)
    for element in soup.select('script, style, nav, footer, .footer, .header, .navigation, .navbar, .menu, .sidebar, iframe, .page_footer, .nav_aside, .search__wrapper'):
        if element:
            element.decompose()
    
    # Удаление комментариев
    for comment in soup.find_all(text=lambda text: isinstance(text, Comment)):
        comment.extract()
    
    # Получение основного контента статьи
    content = None
    
    # Для документации amoCRM, основной контент находится в блоке с классом "content-block__text"
    content = soup.select_one('.content-block__text')
    
    if not content:
        # Альтернативный поиск в других возможных контейнерах
        content_selectors = [
            '.content-block', 
            '.page_section__inner', 
            'article', 
            '.article', 
            'main .page_section', 
            '.article-content'
        ]
        
        for selector in content_selectors:
            content = soup.select_one(selector)
            if content and len(content.get_text(strip=True)) > 100:
                break
    
    # Если ничего не нашли, используем тело документа или main
    if not content:
        content = soup.select_one('main') or soup.body
    
    # Если контент до сих пор не найден, возвращаем пустую строку
    if not content:
        return ""
    
    # Сохраняем правильную обработку кода и предварительно отформатированного текста
    for pre in content.find_all('pre'):
        # Убедимся, что сохраняется форматирование кода
        if pre.find('code'):
            # Если внутри pre есть code, обрабатываем их вместе
            code = pre.find('code')
            # Получаем язык подсветки синтаксиса, если указан
            code_class = code.get('class', [])
            language = ''
            for cls in code_class:
                if cls.startswith('language-'):
                    language = cls.replace('language-', '')
                    break
            
            # Создаем новое содержимое с указанием языка в markdown формате
            code_text = code.get_text()
            new_content = f"```{language}\n{code_text}\n```"
            
            # Заменяем оригинальный pre тег на новое содержимое
            new_tag = soup.new_tag('div')
            new_tag['class'] = 'markdown-code-block'
            new_tag.string = new_content
            pre.replace_with(new_tag)
    
    return str(content) if content else str(soup.body)

def extract_metadata(soup, url):
    """Извлечение метаданных из HTML"""
    metadata = {
        'url': url,
        'title': '',
        'description': '',
        'section': 'support' if '/support' in url else 'developers'
    }
    
    # Извлечение заголовка
    # Первый приоритет: заголовок из content-block__title_large
    title_tag = soup.select_one('.content-block__title_large')
    if title_tag and title_tag.get_text(strip=True):
        metadata['title'] = title_tag.get_text(strip=True)
    else:
        # Второй приоритет: заголовок из тега title
        title_tag = soup.find('title')
        if title_tag:
            metadata['title'] = title_tag.get_text(strip=True)
        else:
            # Третий приоритет: первый h1 на странице
            h1_tag = soup.find('h1')
            if h1_tag:
                metadata['title'] = h1_tag.get_text(strip=True)
    
    # Извлечение описания
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc and meta_desc.get('content'):
        metadata['description'] = meta_desc['content']
    else:
        meta_desc = soup.find('meta', attrs={'name': 'og:description'})
        if meta_desc and meta_desc.get('content'):
            metadata['description'] = meta_desc['content']
    
    # Очистка заголовка от ненужной информации
    metadata['title'] = re.sub(r'^amoCRM\s*[-–—:]\s*', '', metadata['title'])
    
    return metadata

def html_to_markdown(html_content, url):
    """Преобразование HTML в Markdown с метаданными"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Извлечение метаданных
    metadata = extract_metadata(soup, url)
    
    # Очистка HTML
    cleaned_html = clean_html(html_content)
    
    # Если очищенный HTML пустой или слишком короткий, вероятно это не документация
    if not cleaned_html or len(cleaned_html) < 100:
        return None
    
    # Преобразование в Markdown
    # Настройки markdownify для сохранения структуры
    markdown_text = md(cleaned_html, heading_style="ATX", bullets="-", strip=['script', 'style'])
    
    # Обработка специальных блоков кода
    markdown_text = re.sub(r'<div class="markdown-code-block">\s*```(.*?)```\s*</div>', r'```\1```', markdown_text, flags=re.DOTALL)
    
    # Удаление HTML тегов, которые могли остаться
    markdown_text = re.sub(r'<[^>]*>', '', markdown_text)
    
    # Удаление множественных пустых строк
    markdown_text = re.sub(r'\n{3,}', '\n\n', markdown_text)
    
    # Экранирование кавычек в метаданных
    title = metadata['title'].replace('"', "'")
    description = metadata['description'].replace('"', "'")
    
    # Добавление метаданных в начало markdown-файла в виде YAML frontmatter
    frontmatter = f"""---
title: "{title}"
description: "{description}"
url: {metadata['url']}
section: {metadata['section']}
---

"""
    
    return frontmatter + markdown_text

def get_output_filename(html_path, section):
    """Создание имени файла для Markdown на основе исходного HTML-файла"""
    # Получение базового имени файла без расширения
    basename = os.path.basename(html_path)
    filename = os.path.splitext(basename)[0]
    
    # Обработка URL в имени файла
    # Заменяем 'www.amocrm.ru_' или 'amocrm.ru_' на пустую строку
    filename = re.sub(r'(www\.)?amocrm\.ru_', '', filename)
    
    # Замена подчеркиваний на дефисы для более удобочитаемых имен файлов
    filename = filename.replace('_', '-')
    
    # Добавление расширения .md
    return os.path.join(MARKDOWN_PATH, section, f"{filename}.md")

def detect_encoding(file_path):
    """Определение кодировки файла с приоритетом UTF-8"""
    encodings = ['utf-8', 'cp1251', 'latin-1', 'windows-1251']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                f.read()
            return encoding
        except UnicodeDecodeError:
            continue
    
    # Если ничего не подошло, возвращаем UTF-8
    return 'utf-8'

def get_url_from_filename(filename):
    """Извлечение URL из имени файла"""
    # Удаляем расширение .html
    filename = re.sub(r'\.html$', '', filename)
    
    # Если в имени есть домен, заменяем подчёркивания на слеши
    if 'amocrm.ru_' in filename:
        # Заменяем подчёркивания на слеши для путей
        path_part = filename.replace('_', '/')
        
        # Если имя начинается с www, то добавляем https://
        if path_part.startswith('www.'):
            url = f"https://{path_part}"
        else:
            # Иначе добавляем https://www.
            url = f"https://www.{path_part}"
        
        return url
    
    # Если в имени нет домена, предполагаем, что это путь
    return f"https://www.amocrm.ru/{filename.replace('_', '/')}"

def process_html_files(html_dir, section):
    """Обработка всех HTML-файлов в указанной директории"""
    html_files = glob.glob(os.path.join(html_dir, '*.html'))
    logger.info(f"Найдено {len(html_files)} HTML-файлов в {html_dir}")
    
    # Счетчики для статистики
    successful = 0
    skipped = 0
    failed = 0
    
    for html_path in tqdm(html_files, desc=f"Processing {section} files"):
        try:
            # Проверка нужно ли пропустить файл 
            if should_skip_file(html_path):
                logger.info(f"Пропущен файл (бинарный файл): {html_path}")
                skipped += 1
                continue
            
            # Определение кодировки файла
            encoding = detect_encoding(html_path)
            
            # Чтение HTML-файла
            with open(html_path, 'r', encoding=encoding) as f:
                html_content = f.read()
            
            # Извлечение URL из имени файла
            filename = os.path.basename(html_path)
            url = get_url_from_filename(filename)
            
            # Преобразование в Markdown
            markdown_text = html_to_markdown(html_content, url)
            
            # Если markdown_text = None, значит контент не подошел для преобразования
            if markdown_text is None:
                logger.info(f"Пропущен файл (недостаточно контента): {html_path}")
                skipped += 1
                continue
            
            # Сохранение результата
            output_path = get_output_filename(html_path, section)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown_text)
            
            logger.info(f"Обработан файл: {html_path} -> {output_path}")
            successful += 1
            
        except Exception as e:
            logger.error(f"Ошибка при обработке {html_path}: {e}")
            failed += 1
    
    logger.info(f"Статистика обработки {section}: успешно - {successful}, пропущено - {skipped}, ошибки - {failed}")

def main():
    logger.info("Запуск преобразования HTML в Markdown")
    
    # Обработка файлов из раздела support
    if os.path.exists(HTML_SUPPORT_PATH):
        process_html_files(HTML_SUPPORT_PATH, 'support')
    
    # Обработка файлов из раздела developers
    if os.path.exists(HTML_DEV_PATH):
        process_html_files(HTML_DEV_PATH, 'developers')
    
    logger.info("Преобразование завершено")

if __name__ == "__main__":
    main() 