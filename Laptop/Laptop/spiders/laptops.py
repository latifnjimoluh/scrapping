import scrapy
from Laptop.items import LaptopItem
from datetime import datetime

class LaptopsSpider(scrapy.Spider):
    name = "laptops"
    allowed_domains = ["webscraper.io"]
    start_urls = ["https://webscraper.io/test-sites/e-commerce/ajax/computers/laptops"]

         # Compteur de produits
    products_scraped = 0
    
    def parse(self, response):
        """
        Méthode principale pour extraire les données des produits
        
        Args:
            response: La réponse HTML (après traitement par Selenium)
        """
        self.logger.info(f'🔍 Parsing page: {response.url}')
        
        # Sélectionner tous les produits sur la page
        products = response.css('.thumbnail')
        
        self.logger.info(f'Nous avons trouvé {len(products)} produits sur cette page')
        
        # Parcourir chaque produit
        for product in products:
            self.products_scraped += 1
            
            item = LaptopItem()
            
            # 1. Extraire le TITRE (title)
            title = product.css('.title::attr(title)').get()
            if not title:
                title = product.css('.title::text').get()
            item['title'] = title.strip() if title else "N/A"
            
            # 2. Extraire le PRIX (price)
            price_text = product.css('.price::text').get()
            item['price'] = price_text.strip() if price_text else "N/A"
            
            # 3. Extraire la DESCRIPTION (description)
            description = product.css('.description::text').get()
            item['description'] = description.strip() if description else "N/A"
            
            # 4. Extraire le NOMBRE D'AVIS (review_count)
            # Le nombre d'avis est dans .ratings p.pull-right
            review_text = product.css('.ratings p.pull-right::text').get()
            if review_text:
                # Format: "15 reviews" -> extraire "15"
                review_count = review_text.strip().split()[0]
                item['review_count'] = review_count
            else:
                item['review_count'] = "0"
            
            # 5. Extraire la NOTE (rating)
            # Les étoiles sont dans .ratings avec un attribut data-rating
            rating = product.css('.ratings p[data-rating]::attr(data-rating)').get()
            item['rating'] = rating if rating else "0"
            
            
            
            # Ajouter la date/heure du scraping
            item['scraped_at'] = datetime.now().isoformat()
            
            self.logger.info(f'✅ Produit {self.products_scraped}: {item["title"]} - {item["price"]}')
            
            # Yield l'item
            yield item
        
        self.logger.info(f'📊 Total des produits scrapés : {self.products_scraped}')
