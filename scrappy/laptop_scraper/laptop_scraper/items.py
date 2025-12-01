import scrapy

class LaptopItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    reviews = scrapy.Field()
    rating = scrapy.Field()
