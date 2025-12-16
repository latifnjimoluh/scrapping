# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LaptopItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()          # Nom du produit
    price = scrapy.Field()           # Prix
    description = scrapy.Field()     # Description
    rating = scrapy.Field()     # Note (reviews)
    review_count = scrapy.Field() # Nombre d'avis
    image_url = scrapy.Field()       # URL de l'image
    product_url = scrapy.Field()     # URL du produit
    scraped_at = scrapy.Field()      # Date/heure du scraping
    pass
