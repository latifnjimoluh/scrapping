import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# 📌 Liste des animes à capturer
ANIME_LIST = [
    "Jujutsu Kaisen",
    "Solo Leveling",
    "Tokyo Ghoul",
    "Bleach",
    "Naruto",
    "Chainsaw Man",
    "One Piece"
]


def capture_for_anime(anime_name):
    print(f"\n==============================")
    print(f"🎬 Capture pour : {anime_name}")
    print("==============================")

    # 🔎 Construire l'URL de recherche YouTube
    query = anime_name.replace(" ", "+")
    url = f"https://www.youtube.com/results?search_query={query}"

    # 📁 Créer un dossier "captures"
    folder = "captures"
    os.makedirs(folder, exist_ok=True)

    # 🕒 Générer un nom unique
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    safe_name = anime_name.replace(" ", "_")
    file_path = f"{folder}/{safe_name}_{timestamp}.png"

    # ⚙️ Configurer Selenium
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    print("🌐 Ouverture de YouTube...")
    driver.get(url)

    try:
        # Attendre que les résultats apparaissent
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "contents"))
        )
        print("📺 Vidéos chargées")

        # Scroll pour charger plus de contenu visuel
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # 📸 Capture d'écran
        driver.save_screenshot(file_path)
        print(f"✅ Capture enregistrée : {file_path}")

    except Exception as e:
        print("❌ Erreur :", e)

    finally:
        driver.quit()



# 🚀 PROGRAMME PRINCIPAL : capture pour tous les animes
for anime in ANIME_LIST:
    capture_for_anime(anime)

print("\n🎉 Toutes les captures ont été générées avec succès !")
