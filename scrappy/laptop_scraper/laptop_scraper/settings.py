BOT_NAME = "laptop_scraper"

SPIDER_MODULES = ["laptop_scraper.spiders"]
NEWSPIDER_MODULE = "laptop_scraper.spiders"

ROBOTSTXT_OBEY = False

# IMPORTANT : Scrapy doit aller lentement pour Selenium
CONCURRENT_REQUESTS = 1
DOWNLOAD_DELAY = 1
RANDOMIZE_DOWNLOAD_DELAY = True

# USER AGENT réaliste
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"

# On active le middleware Selenium
DOWNLOADER_MIDDLEWARES = {
    "laptop_scraper.selenium_middleware.SeleniumMiddleware": 543,
}

ITEM_PIPELINES = {
    "laptop_scraper.pipelines.LaptopScraperPipeline": 300,
}

LOG_LEVEL = "ERROR"
