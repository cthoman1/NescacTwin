from bs4 import BeautifulSoup
import requests
from datetime import datetime
import sqlite3

url = 'https://www.tfrrs.org/athletes/7820846/Bates/Colin_Thoman.html'
page = requests.get(url)
soup = BeautifulSoup(page.text, features="html.parser")
tables = soup.find_all('table', class_='table table-hover >')

data = []

for table in tables:
    date_span = table.find_previous('span', style='color:black;font-size:14px;')
    if date_span:
        date_string = date_span.text.strip()
        if '-' in date_string:
            date_string = date_string.split('-')[0].strip() + date_string[-6:]
        date_obj = datetime.strptime(date_string, '%b %d, %Y')
        date_mmddyy = date_obj.strftime('%m/%d/%y')
    else:
        date_mmddyy = ''  # Handle case where date span is not found or date_string cannot be parsed
    rows = table.find_all('tr')
    for row in rows:
        event_td = row.find('td', class_='panel-heading-text')
        if event_td:
            event = event_td.text.strip()
        else:
            event = ''
    columns = row.find_all('td')
    result = columns[1].text.strip() if len(columns) > 1 else ''
    if date_mmddyy:
        data.append((date_mmddyy, event, result))


conn = sqlite3.connect('tfrrsresults.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS athletes (
    athlete_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS race_results (
    id INTEGER PRIMARY KEY,
    FOREIGN KEY (athlete_id) REFERENCES athletes (athlete_id)
    race_date DATE,
    event TEXT,
    result TEXT
)
''')

for entry in data:
    cursor.execute('''
    INSERT INTO race_results (date, event, result)
    VALUES (?, ?, ?)
    ''', entry)

for entry in data:
    cursor.execute('''
    INSERT INTO athletes (name)
    VALUES (?)
    ''', entry)

conn.commit()
