import csv
import os

class LaptopScraperPipeline:

    def open_spider(self, spider):
        os.makedirs("output", exist_ok=True)
        self.file = open("output/laptops.csv", "w", newline="", encoding="utf-8")
        self.writer = csv.writer(self.file)
        self.writer.writerow(["Title", "Price", "Description", "Reviews", "Rating"])

    def process_item(self, item, spider):
        self.writer.writerow([
            item["title"],
            item["price"],
            item["description"],
            item["reviews"],
            item["rating"]
        ])
        return item

    def close_spider(self, spider):
        self.file.close()
