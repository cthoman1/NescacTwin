from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
import time



# The idea here will be to make a webdriver script that gets the homepage from the school name.
# It will do this by just googling for it and clicking the first link.


print(get_homepage_url('Bates'))