from bs4 import BeautifulSoup
import requests
import csv

# URL de la page
url = "https://www.scrapethissite.com/pages/simple/"

# Récupération de la page
response = requests.get(url)
html_content = response.text

# Parsing avec BeautifulSoup
soup = BeautifulSoup(html_content, "lxml")

# Sélection de tous les blocs pays
countries = soup.find_all("div", class_="col-md-4 country")

# Création du fichier CSV
with open("countries.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Country", "Capital", "Population", "Area"])

    # Extraction des données
    for country in countries:
        name = country.find("h3", class_="country-name").get_text(strip=True)
        capital = country.find("span", class_="country-capital").get_text(strip=True)
        population = country.find("span", class_="country-population").get_text(strip=True)
        area = country.find("span", class_="country-area").get_text(strip=True)

        # Écriture dans le CSV
        writer.writerow([name, capital, population, area])

print("Scraping terminé ! Fichier countries.csv créé.")
