import scrapy
from laptop_scraper.items import LaptopItem
import re

class LaptopsSpider(scrapy.Spider):
    name = "laptops"
    allowed_domains = ["webscraper.io"]
    start_urls = [
        "https://webscraper.io/test-sites/e-commerce/ajax/computers/laptops"
    ]

    page_number = 1

    def parse(self, response):

        print(f"\n📄 Chargement de la page {self.page_number}...")

        products = response.css(".thumbnail")
        print(f"   ➜ {len(products)} produits trouvés.")

        # Extraction
        for p in products:
            item = LaptopItem()

            item["title"] = p.css(".title::text").get().strip()
            item["price"] = p.css(".price::text").get().strip()
            item["description"] = p.css(".description::text").get().strip()
            item["reviews"] = p.css(".ratings .pull-right::text").get().strip()
            item["rating"] = len(p.css(".glyphicon-star"))

            yield item

        # Pagination : détecter le nombre total de pages
        page_buttons = response.css("button.page-link.page::attr(data-id)").getall()
        total_pages = len(page_buttons)

        if self.page_number < total_pages:
            self.page_number += 1
            next_url = f"{self.start_urls[0]}?page={self.page_number}"

            print(f"➡️ Passage à la page {self.page_number}...")

            yield scrapy.Request(next_url, callback=self.parse)

        else:
            print("\n✅ Scraping terminé ! Toutes les pages ont été traitées.")
