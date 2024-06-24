from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
import time
import re
from scrape import get_athlete_urls
athlete_urls = []
season_urls = ['https://www.tfrrs.org/teams/tf/ME_college_m_Bates.html?config_hnd=335', 'https://www.tfrrs.org/teams/tf/ME_college_m_Bates.html?config_hnd=292']
for season_url in season_urls:
    athlete_urls.append(get_athlete_urls(season_url))

print(athlete_urls)

