from datetime import datetime
import requests
from bs4 import BeautifulSoup

def scrape_athlete_data(athlete_id):
    url = f"https://www.tfrrs.org/athletes/{athlete_id}.html"
    page = requests.get(url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, features="html.parser")
        tables = soup.find_all('table', class_='table table-hover >')
# defining tables as long text string of text parsed from tfrrs results page
# good to mention here that xc times have a different class, that being 'table table hover xc'
        data = []
        name = ''
        school = ''
#defining "data" as empty dataset
        header_elements = soup.find_all('h3', class_='panel-title')
        for elem in header_elements:
            if 'large-title' not in elem.get('class', []):
                school = elem.text.strip().title()
            else:
                name = elem.text.strip().title()[:-7]
        for table in tables:
            date_span = table.find_previous('span', style='color:black;font-size:14px;')
#defining date_span as every instance where the date style is used on text
            if date_span:
                date_string = date_span.text.strip()
#defining date_string as the text stripped version of date_span
                if '-' in date_string:
                    date_string = date_string.split('-')[0].strip() + date_string[-6:]
                date_obj = datetime.strptime(date_string, '%b %d, %Y')
                race_date = date_obj.strftime('%m/%d/%y')
#setting date ranges to show just the first day of the range, then changing the format of the date to mm/dd/yy
            else:
                race_date = ''
#contingency for empty date field
            rows = table.find_all('tr')
#defining rows as every instance where tr is used, which includes pretty much all results
            for row in rows:
                event_td = row.find('td', class_='panel-heading-text')
                if event_td:
                    event = event_td.text.strip()
                else:
                    event = ''
            columns = row.find_all('td')
            result = columns[1].text.strip() if len(columns) > 1 else ''
            if race_date and event and result:
                data.append((race_date, event, result))
        return name, school, data
    else:
        return None, None, None
athlete_id = 7820846
name = scrape_athlete_data(athlete_id)[0]
school = scrape_athlete_data(athlete_id)[1]
data = scrape_athlete_data(athlete_id)[2]


import sqlite3

conn = sqlite3.connect('tfrrsresults.db')
cursor = conn.cursor()
conn.execute('PRAGMA foreign_keys = ON;')

cursor.execute('''
CREATE TABLE IF NOT EXISTS athletes (
    athlete_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);
''')

cursor.execute('''
INSERT INTO athletes (athlete_id,name)
VALUES (?,?)
''', (athlete_id, name))

cursor.execute('''
CREATE TABLE IF NOT EXISTS race_results ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    athlete_id INTEGER,
    race_date DATE,
    event TEXT,
    result TEXT,
    FOREIGN KEY (athlete_id) REFERENCES athletes (athlete_id)
)
''')

cursor.execute('DELETE FROM race_results;')

cursor.execute('DELETE FROM athletes;')
#clears existing
for entry in data:
    cursor.execute('''
    INSERT INTO race_results (race_date, event, result)
    VALUES (?, ?, ?)
    ''', (entry[0], entry[1], entry[2]))

conn.commit()
conn.close

