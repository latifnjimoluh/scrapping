# selenium_middleware.py

from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class SeleniumMiddleware:

    def __init__(self):
        """Initialisation du navigateur Selenium"""
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_request(self, request, spider):
        """Intercepte les requêtes Scrapy et utilise Selenium pour charger la page."""

        self.driver.get(request.url)

        # Attendre que les produits (JS) soient chargés
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".thumbnail"))
            )
        except:
            pass

        # Gérer la bannière cookies
        try:
            cookie_btn = self.driver.find_element(By.CSS_SELECTOR, "button.acceptCookies")
            cookie_btn.click()
            time.sleep(1)
        except:
            pass

        body = self.driver.page_source

        return HtmlResponse(
            self.driver.current_url,
            body=body,
            encoding='utf-8',
            request=request
        )
