# utils/browser.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from config import PAGE_LOAD_WAIT

def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # retirer si tu veux voir le navigateur
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver


def get_rendered_html(driver, url):
    driver.get(url)
    time.sleep(PAGE_LOAD_WAIT)
    return driver.page_source
