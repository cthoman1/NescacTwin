from dbfunctions import save_to_db
from dbfunctions import clear_database
import time
from scrape import scrape_athlete_data
from scrape import get_homepage_url
from scrape import get_season_urls
import requests
from scrape import get_public_ip


public_ip = get_public_ip()
print(f'Public IP:{public_ip}')


schools = ["Bates"]
homepage_urls = []
for school in schools:
    homepage_urls.append(get_homepage_url(school))
    season_urls = []
    for homepage_url in homepage_urls:
        season_urls.append(get_season_urls(homepage_url))
        athlete_urls = []


