from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
import time
import re



def get_season_urls(homepage):
    chrome_driver_path = '/Users/colinthoman/Downloads/chromedriver-mac-arm64/chromedriver'
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service)
    driver.get(homepage)
    season_codes = []
    season_urls = []
    try:
        dropdown_div = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.CLASS_NAME, 'col-lg-4.pt-5'))
        )
        dropdown = dropdown_div.find_element(By.TAG_NAME, 'select')
        options = dropdown.find_elements(By.TAG_NAME, 'option')
        last_option = options[-1]
        for option in options:
            try:
                season_code = option.get_attribute('value')
                if season_code:
                    season_codes.append(season_code)
            except StaleElementReferenceException:
                continue
            except Exception as e:
                print(f"Error during iteration: {type(e).__name__}")
                continue
        last_option.click()
        earliest_season_url = driver.current_url
        season_code_pattern = r'(hnd=)\d+'
        for season_code in season_codes:
            season_url = re.sub(season_code_pattern, 'hnd='+season_code, earliest_season_url)
            season_urls.append(season_url)
        return season_urls
    except Exception as e:
        print(f"Error: {e}")
    driver.quit()


print(get_season_urls('https://www.tfrrs.org/teams/tf/ME_college_m_Bates.html'))

