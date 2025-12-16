from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class LaptopDownloaderMiddleware:

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        # Driver
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_request(self, request, spider):
        spider.logger.info(f"🌐 Selenium charge la page : {request.url}")

        self.driver.get(request.url)

        # Gérer la bannière cookies
        try:
            accept_btn = WebDriverWait(self.driver, 4).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".acceptCookies"))
            )
            accept_btn.click()
            spider.logger.info("🍪 Cookies acceptés")
        except:
            pass

        # Attendre les produits
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".thumbnail"))
            )
            spider.logger.info("📦 Produits chargés avec succès")
        except:
            spider.logger.warning("⚠️ Les produits ne se chargent pas")

        # Retourner la page rendue
        html = self.driver.page_source
        return HtmlResponse(
            self.driver.current_url,
            body=html,
            encoding='utf-8',
            request=request
        )

    def __del__(self):
        try:
            self.driver.quit()
        except:
            pass
