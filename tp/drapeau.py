from bs4 import BeautifulSoup
import requests
import csv
import base64

# URL du site
url = "https://www.drapeauxdespays.fr/registration"

# Récupération de la page
response = requests.get(url)
soup = BeautifulSoup(response.text, "lxml")

# Sélection des éléments <li> contenant les pays
countries = soup.find_all("li")

# On limite à 10 drapeaux
countries = countries[:100]

# Création du CSV
with open("flags_in_csv.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Country", "Flag_Base64"])

    # Extraction
    for country in countries:
        link = country.find("a")
        img = country.find("img")

        if not link or not img:
            continue

        # Nom du pays
        name = link.get_text(strip=True)

        # URL du drapeau
        img_url = img["src"]
        if img_url.startswith("/"):
            img_url = "https://www.drapeauxdespays.fr" + img_url

        # Télécharger l'image
        img_data = requests.get(img_url).content

        # Encoder en Base64
        img_b64 = base64.b64encode(img_data).decode("utf-8")

        # Écrire dans le CSV
        writer.writerow([name, img_b64])

        print(f"{name} ajouté au CSV.")

print("Scraping terminé ! Les 10 drapeaux sont enregistrés dans flags_in_csv.csv.")
