import os
import csv
import time
from multiprocessing import Pool, cpu_count

from tqdm import tqdm
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from utils.browser import create_driver
from utils.parser import parse_laptops
from config import BASE_URL


def handle_cookies(driver):
    try:
        btn = driver.find_element(By.CSS_SELECTOR, "button.acceptCookies")
        btn.click()
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


# ========= WORKER PROCESS FUNCTION =========
def scrape_single_page(page_num):
    """
    Chaque process :
    - lance un driver
    - va sur le site
    - clique sur la page
    - scrape les produits
    - renvoie le résultat
    """

    driver = create_driver()
    driver.get(BASE_URL)
    time.sleep(2)

    # cookies si présents
    try:
        handle_cookies(driver)
    except:
        pass

    try:
        page_btn = driver.find_element(
            By.CSS_SELECTOR, f'button.page-link.page[data-id="{page_num}"]'
        )

        driver.execute_script("arguments[0].click();", page_btn)
        time.sleep(2)

        html = driver.page_source
        products = parse_laptops(html)

        print(f" → Page {page_num} : {len(products)} produits.")

    except Exception as e:
        print(f"⚠️ Erreur page {page_num}: {e}")
        products = []

    driver.quit()
    return products


def main():
    print("🚀 Initialisation du navigateur principal...")
    driver = create_driver()
    driver.get(BASE_URL)
    time.sleep(2)
    handle_cookies(driver)

    print("\n📌 Détection du nombre total de pages...")
    page_buttons = driver.find_elements(By.CSS_SELECTOR, "button.page-link.page")
    total_pages = len(page_buttons)

    driver.quit()  # browser principal fermé après détection des pages

    print(f"➡️ Il y a {total_pages} pages à scraper.\n")

    # CPU - 1 pour éviter de saturer la machine
    max_workers = max(1, cpu_count() - 1)
    print(f" Utilisation de {max_workers} processus.\n")

    all_products = []

    # ========== MULTIPROCESSING ==========
    with Pool(processes=max_workers) as pool:
        results = list(
            tqdm(pool.imap(scrape_single_page, range(1, total_pages + 1)),
                 total=total_pages,
                 desc="Scraping en parallèle")
        )

    # fusion des résultats
    for page_data in results:
        all_products.extend(page_data)

    save_to_csv(all_products)

    print(f"\n🟢 Terminé. Total produits : {len(all_products)}")


if __name__ == "__main__":
    main()
