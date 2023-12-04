import openpyxl
from service import *

# Соберем urls из файла 'страницы.txt'
URLs = get_urls('страницы.txt')

# # Создадим файл с пустой таблицей
# create_excel_sample("data.xlsx")

def main():
    # Загружаем уже существующую таблицу
    workbook = openpyxl.load_workbook('data.xlsx')

    # Выбираем активный лист
    sheet = workbook.active
    
    # Соберем уже добавленные в таблицу страницы, чтобы не дублировать
    parsed_urls = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        parsed_urls.append(row[0])
    
    # Пройдемся по каждому url и добавим данные в таблицу
    for url in URLs:
        
        # Если страница уже в таблице, то пропускаем ее парсинг
        if url in parsed_urls:
            continue
        
        # Получаем HTML-код страницы
        try:
            html = get_html_code(url)
        except Exception as er:
            logger.error(er)
        
        data = {}
        
        # Добавим в словарь значения по атрибутам
        for key in ["lang", "charset"]:
            try:
                data[key] = ','.join(get_values_by_attr(html, key))
            except Exception as er:
                logger.error(er)
                
        # Добавим в словарь значения по тегам
        for key in ["title", "h1", "h2", "h3", "h4", "h5", "h6"]:
            try:
                data[key] = ','.join(get_text_by_tag(html, key))
            except Exception as er:
                logger.error(er)
                        
        # Добавим в словарь значения по name=? или property=?
        for key in ['viewport', 'description', 'keywords', 'currency',
                    'og:title', 'og:description', 'og:site_name', 'og:type',
                    'og:url', 'og:image']:
            try:
                data[key] = ','.join(get_content_by_value(html, key))
            except Exception as er:
                logger.error(er)
            
        # Добавим в словарь значения по rel='canonical'
        try:
            data['canonical'] = ','.join(get_href_by_rel(html))
        except Exception as er:
            logger.error(er)
        
        # Добавляем ряд значений
        sheet.append([url] + list(data.values()))
        
    # Сохраняем XLSX файл
    workbook.save("data.xlsx")


if __name__ == '__main__':
    main()