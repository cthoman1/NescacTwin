from save_to_db import save_to_db
from save_to_db import clear_database
import time
from scrape import scrape_athlete_data

athlete_ids = [7820847]
# This is toga

clear_database()
for athlete_id in athlete_ids:
    save_to_db(athlete_id)
    time.sleep(.5)

