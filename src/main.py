from dbfunctions import save_to_db
from dbfunctions import clear_database
import time
import random
from scrape import get_homepage_url
from scrape import get_season_urls
from scrape import get_athlete_urls
from scrape import get_public_ip
from dbfunctions import update_event_names_to_codes
from dbfunctions import create_event_code_reference_table


# public_ip = get_public_ip()
# print(f'Public IP:{public_ip}')

# clear_database()
'''
schools = ['Colby']
homepage_urls = []
for school in schools:
    homepage_urls.append(get_homepage_url(school))
    season_urls = []
    for homepage_url in homepage_urls:
        season_urls = get_season_urls(homepage_url)
        athlete_urls = set()
        for season_url in season_urls:
            athlete_urls.update(get_athlete_urls(season_url))
        athlete_urls = list(athlete_urls)
        for athlete_url in athlete_urls:
            save_to_db(athlete_url)
            time.sleep(random.uniform(10, 20))
print("Operation was completed without any errors.")'''

create_event_code_reference_table('nescactf.db')
update_event_names_to_codes('nescactf.db')
