# scraper.py

import os
import csv
import time
from tqdm import tqdm
from selenium.webdriver.common.by import By
from utils.browser import create_driver
from utils.parser import parse_laptops
from config import BASE_URL
from selenium.common.exceptions import NoSuchElementException


def handle_cookies(driver):
    """Ferme la bannière des cookies si elle apparaît."""
    try:
        cookie_button = driver.find_element(By.CSS_SELECTOR, "button.acceptCookies")
        cookie_button.click()
        print("🍪 Cookies acceptés.")
        time.sleep(1)
    except NoSuchElementException:
        pass


def save_to_csv(data, filename="output/laptops.csv"):
    os.makedirs("output", exist_ok=True)

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Price", "Description", "Reviews", "Rating"])

        for item in data:
            writer.writerow([
                item["title"],
                item["price"],
                item["description"],
                item["review_count"],
                item["rating"]
            ])

    print(f"\n💾 CSV généré : {filename}")


def main():
    print("🚀 Initialisation du navigateur...")
    driver = create_driver()

    driver.get(BASE_URL)
    time.sleep(2)
    handle_cookies(driver)

    print("\n📌 Détection du nombre total de pages...")
    page_buttons = driver.find_elements(By.CSS_SELECTOR, "button.page-link.page")
    total_pages = len(page_buttons)

    print(f"➡️ Il y a {total_pages} pages à scraper.\n")

    all_products = []

    # ========= BOUCLE SUR CHAQUE PAGE ==========
    for page_num in tqdm(range(1, total_pages + 1), desc="Progression"):
        try:
            # Cibler le bouton par data-id
            page_btn = driver.find_element(By.CSS_SELECTOR, f'button.page-link.page[data-id="{page_num}"]')

            driver.execute_script("arguments[0].click();", page_btn)
            time.sleep(2)

            print(f"\n📄 Page {page_num} — scraping...")

            # Scraper cette page
            html = driver.page_source
            products = parse_laptops(html)

            print(f"   → {len(products)} produits trouvés sur cette page.")

            all_products.extend(products)

        except Exception as e:
            print(f"⚠️ Erreur sur la page {page_num} : {e}")

    save_to_csv(all_products)
    driver.quit()


if __name__ == "__main__":
    main()
