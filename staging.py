from dbfunctions import save_to_db
from dbfunctions import clear_database
import time
import random
from scrape import get_homepage_url
from scrape import get_season_urls
from scrape import get_athlete_urls
from scrape import scrape_athlete_data
from scrape import get_athlete_urls
from dbfunctions import save_to_db


save_to_db('https://www.tfrrs.org/athletes/7912185/Bates/Aidan_Rooney')
# time.sleep(random.uniform(10, 20))
