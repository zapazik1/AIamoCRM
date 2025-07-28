import requests
from bs4 import BeautifulSoup
import os
import time
import re
import urllib.parse
import random
import logging
from tqdm import tqdm

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join('database', 'scraper.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Константы
BASE_SUPPORT_URL = 'https://www.amocrm.ru/support'
BASE_DEV_URL = 'https://www.amocrm.ru/developers/content/crm_platform/platform-abilities'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
HEADERS = {
    'User-Agent': USER_AGENT,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
}

# Пути для сохранения файлов
SUPPORT_PATH = os.path.join('database', 'raw_html', 'support')
DEV_PATH = os.path.join('database', 'raw_html', 'developers')

# Проверка и создание директорий, если они не существуют
os.makedirs(SUPPORT_PATH, exist_ok=True)
os.makedirs(DEV_PATH, exist_ok=True)

# Функция для нормализации URL
def normalize_url(url):
    # Удаление якорей
    url = re.sub(r'#.*$', '', url)
    # Удаление параметров запроса
    url = re.sub(r'\?.*$', '', url)
    # Возвращаем URL без завершающего слеша
    return url.rstrip('/')

# Функция для создания имени файла из URL
def url_to_filename(url):
    # Удаляем протокол
    filename = re.sub(r'^https?://', '', url)
    # Заменяем слеши и специальные символы
    filename = re.sub(r'[\\/:*?"<>|]', '_', filename)
    # Добавляем расширение .html
    return f"{filename}.html"

# Функция для проверки, что URL относится к нужному домену
def is_valid_url(url, base_domain='amocrm.ru'):
    return base_domain in url

# Функция для получения HTML-страницы
def get_page(url, retry_count=3):
    for attempt in range(retry_count):
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            logger.warning(f"Попытка {attempt+1}/{retry_count} для {url} не удалась: {e}")
            time.sleep(2 ** attempt)  # Экспоненциальная задержка
    
    logger.error(f"Не удалось загрузить {url} после {retry_count} попыток")
    return None

# Функция для извлечения ссылок из HTML
def extract_links(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    
    for a in soup.find_all('a', href=True):
        href = a['href']
        
        # Пропускаем ссылки на javascript и якори
        if href.startswith('javascript:') or href.startswith('#'):
            continue
        
        # Преобразование относительного URL в абсолютный
        if href.startswith('/'):
            href = urllib.parse.urljoin(base_url, href)
        elif not href.startswith('http'):
            href = urllib.parse.urljoin(base_url, href)
        
        # Нормализация URL
        href = normalize_url(href)
        
        # Проверка, что URL относится к домену amocrm.ru
        if is_valid_url(href):
            links.append(href)
    
    # Особая обработка для базы знаний amoCRM
    if 'support' in base_url:
        # Находим все категории и разделы
        categories = soup.select('.categories-list a, .section-list a, .article-list a, .knowledge-base a')
        for category in categories:
            href = category.get('href')
            if href:
                # Преобразование относительного URL в абсолютный
                if href.startswith('/'):
                    href = urllib.parse.urljoin(base_url, href)
                
                # Нормализация URL
                href = normalize_url(href)
                
                if is_valid_url(href):
                    links.append(href)
    
    return list(set(links))  # Удаление дубликатов

# Функция для сохранения HTML в файл
def save_html(html, url, base_path):
    filename = url_to_filename(url)
    filepath = os.path.join(base_path, filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        logger.info(f"Сохранен файл: {filepath}")
        return True
    except Exception as e:
        logger.error(f"Ошибка при сохранении {filepath}: {e}")
        return False

# Функция для веб-краулинга
def crawl(base_url, save_path, max_pages=500):
    visited = set()
    to_visit = [base_url]
    
    logger.info(f"Начинаем краулинг для {base_url}")
    
    with tqdm(desc=f"Crawling {base_url}", unit="page") as progress:
        while to_visit and len(visited) < max_pages:
            url = to_visit.pop(0)
            
            # Пропускаем уже посещенные URL
            if url in visited:
                continue
            
            # Маркируем URL как посещенный
            visited.add(url)
            
            # Получаем HTML-страницу
            html = get_page(url)
            if html is None:
                continue
            
            # Сохраняем HTML
            save_html(html, url, save_path)
            
            # Извлекаем ссылки
            links = extract_links(html, base_url)
            
            # Отфильтровываем ссылки по заданным разделам
            if 'support' in base_url:
                links = [link for link in links if '/support' in link]
            elif '/developers/' in base_url:
                links = [link for link in links if '/developers/' in link]
            
            # Добавляем новые ссылки в очередь
            for link in links:
                if link not in visited and link not in to_visit:
                    to_visit.append(link)
            
            # Обновляем прогресс
            progress.update(1)
            progress.set_postfix(visited=len(visited), queue=len(to_visit))
            
            # Задержка между запросами
            time.sleep(random.uniform(1.0, 2.0))
    
    logger.info(f"Краулинг завершен для {base_url}. Всего посещено страниц: {len(visited)}")
    return visited

def main():
    logger.info("Запуск скрапера amoCRM")
    
    # Краулинг Базы Знаний
    logger.info("Начинаем сбор данных из Базы Знаний amoCRM")
    support_visited = crawl(BASE_SUPPORT_URL, SUPPORT_PATH)
    
    # Краулинг документации для разработчиков
    logger.info("Начинаем сбор данных из документации для разработчиков amoCRM")
    dev_visited = crawl(BASE_DEV_URL, DEV_PATH)
    
    # Статистика
    logger.info(f"Всего собрано страниц из Базы Знаний: {len(support_visited)}")
    logger.info(f"Всего собрано страниц из документации для разработчиков: {len(dev_visited)}")
    logger.info("Скрапинг завершен")

if __name__ == "__main__":
    main() 