from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re
from cleaning import remove_imperial
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

school_url = 'https://www.tfrrs.org/teams/tf/ME_college_m_Bates.html?config_hnd=335'


def get_athlete_links(school_url):
    response = requests.get(school_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    roster_header = soup.find('h3', string='ROSTER')
    if roster_header:
        roster_table = roster_header.find_next('table')
        if roster_table:
            athlete_urls = []
            rows = roster_table.find_all('tr')
            for row in rows:
                link = row.find('a', href=True)
                if link:
                    athlete_url = link['href']
                    athlete_urls.append(athlete_url)
            for url in athlete_urls:
                print(url)
    else:
        print('Roster table not found.')


get_athlete_links(school_url)


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
                name = elem.text.strip()
                name = re.sub(r'\([^)]*\)', '', name).strip().title()
        for table in tables:
            date_span = table.find('span', style='color:black;font-size:14px;')
# defining date_span as every instance where the date style is used on text
            if date_span:
                date_string = date_span.text.strip()
# defining date_string as the text stripped version of date_span
                if '-' in date_string:
                    date_string = date_string.split('-')[0].strip() + date_string[-6:]
                date_obj = datetime.strptime(date_string, '%b %d, %Y')
                race_date = date_obj.strftime('%m/%d/%y')
# setting date ranges to show just the first day of the range, then changing the format of the date to mm/dd/yy
            else:
                race_date = ''
# contingency for empty date field
            rows = table.find_all('tr')
# defining rows as every instance where tr is used, which includes pretty much all results
            for row in rows:
                event_td = row.find('td', class_='panel-heading-text')
                if event_td:
                    event = event_td.text.strip()
                else:
                    event = ''
                columns = row.find_all('td')
                result = columns[1].text.strip() if len(columns) > 1 else ''
                result = remove_imperial(result)
                if race_date and event and result:
                    data.append((race_date, event, result))
        return name, school, data
    else:
        return None, None, None,
        print(f"No data found for {athlete_id}")
