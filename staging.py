from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from scrape import get_athlete_links

school_url = 'https://www.tfrrs.org/teams/tf/ME_college_m_Bates.html?config_hnd=335'


def get_season_codes(url):
    chrome_driver_path = '/Users/colinthoman/Downloads/chromedriver-mac-arm64/chromedriver'
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    try:
        dropdown_div = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.CLASS_NAME, 'col-lg-4.pt-5'))
        )
        dropdown = dropdown_div.find_element(By.TAG_NAME, 'select')
        options = dropdown.find_elements(By.TAG_NAME, 'option')
        season_codes = []
        for option in options:
            season_code = option.get_attribute('value')
            if season_code:
                season_codes.append(season_code)
        return season_codes
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()


def get_season_url(state_abbr,gender_abbr,school,season_code):
    season_url = f'https://www.tfrrs.org/teams/tf/{state_abbr}_college_{gender_abbr}_{school}.html?config_hnd={season_code}'
    return season_url
