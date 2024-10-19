from bs4 import BeautifulSoup
import pandas as pd

# Чтение HTML файла
with open('./fff.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Создаем объект BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Находим таблицу по тегу <table>
table = soup.find('table', {'border': '1'})

# Извлекаем заголовки таблицы, очищая от пробелов и табуляций
headers = [th.get_text(separator=' ').strip() for th in table.find_all('th')]

# Инициализируем список для строк данных
rows = []

# Проходим по каждой строке данных
for row in table.find_all('tr')[1:]:
    # Извлекаем ячейки и очищаем текст
    cells = [td.get_text(separator=' ').strip().replace('\t', '') for td in row.find_all('td')]

    # Проверка на соответствие количества ячеек заголовкам
    if len(cells) < len(headers):
        # Дополняем пустыми значениями, если ячеек меньше
        cells.extend([''] * (len(headers) - len(cells)))
    elif len(cells) > len(headers):
        # Обрезаем лишние ячейки, если их больше
        cells = cells[:len(headers)]

    rows.append(cells)

# Создаем DataFrame с корректными данными
df = pd.DataFrame(rows, columns=headers)

# Сохраняем DataFrame в CSV файл
df.to_csv('parsed_data.csv', index=False, encoding='utf-8')

print("Таблица успешно извлечена и сохранена в 'parsed_data.csv'")
