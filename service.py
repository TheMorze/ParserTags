import requests, openpyxl
from bs4 import BeautifulSoup as BS

from loguru import logger

def get_html_code(url: str) -> str:
    """Получает HTML-код страницы по url"""
    
    request = requests.get(url)
    logger.debug(f'Код подключения к странице: {request.status_code}')
    return request.text

def get_values_by_attr(html: str, attr):
    """Парсит значения по заданному атрибуту HTML"""
    
    soup = BS(html, 'html.parser')
    by_attr = soup.find_all(attrs={attr: True})
    return list(set([el[attr].strip() for el in by_attr])) or ['-']

def get_text_by_tag(html: str, tag):
    """Парсит текст по заданному тегу HTML"""
    
    soup = BS(html, 'html.parser')
    by_tag = soup.find_all(tag)
    return list(set([el.text.strip() for el in by_tag])) or ['-']

def get_content_by_value(html: str, value: str):
    """Парсит значения атрибута content,
    где name=<value> или property=<value>"""
    
    soup = BS(html, 'html.parser')
    by_name = soup.find_all(attrs={'name': value})
    by_property = soup.find_all(attrs={'property': value})
    by_both = by_name + by_property
    return list(set([el['content'].strip() for el in by_both])) or ['-']

def get_href_by_rel(html: str, value='canonical'):
    """Парсит атрибут href в элементах, где rel=<value>
    (по умолчанию rel='canonical')"""
    
    soup = BS(html, 'html.parser')
    by_rel = soup.find_all(attrs={'rel': value})
    return list(set([el['href'].strip() for el in by_rel])) or ['-']
    
def create_excel_sample(name: str):
    """Используется для создания Excel-файла"""
    wb = openpyxl.Workbook()
    
    sheet = wb.active
    sheet.title = 'Данные тегов'
    headers = ["Адрес страницы", "lang", "charset",
               "title", "h1", "h2", "h3", "h4", "h5", "h6",
               'viewport', 'description', 'keywords', 'currency',
               'og:title', 'og:description', 'og:site_name', 'og:type',
               'og:url', 'og:image', 'canonical']
    
    sheet.append(headers)
    
    wb.save(name)
    logger.info('Таблица была создана!')
    
def get_urls(path: str):
    """Собирает ссылки из указанного файла"""
    with open(path, encoding='U8') as file:
        urls = [line.strip() for line in file.readlines()]
    logger.info('Ссылки из файла получены.')
    return urls
