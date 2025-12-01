# utils/parser.py

from bs4 import BeautifulSoup

def parse_laptops(html):
    soup = BeautifulSoup(html, "lxml")
    items = soup.select(".thumbnail")

    results = []
    for item in items:
        title = item.select_one(".title").get_text(strip=True)
        price = item.select_one(".price").get_text(strip=True)
        description = item.select_one(".description").get_text(strip=True)
        reviews = item.select_one(".ratings .pull-right").get_text(strip=True)
        rating = len(item.select(".glyphicon-star"))

        results.append({
            "title": title,
            "price": price,
            "description": description,
            "review_count": reviews,
            "rating": rating
        })

    return results
