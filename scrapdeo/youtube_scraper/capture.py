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


def capture_for_anime(anime_name="anime trailer"):
    print(f"\n==============================")
    print(f"🎬 Capture pour : {anime_name}")
    print("==============================")

    query = anime_name.replace(" ", "+")
    url = f"https://www.youtube.com/results?search_query={query}"

    folder = "captures"
    os.makedirs(folder, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    safe_name = anime_name.replace(" ", "_")
    file_path = f"{folder}/{safe_name}_{timestamp}.png"

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
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "contents"))
        )
        print("📺 Vidéos chargées")

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        driver.save_screenshot(file_path)
        print(f"✅ Capture enregistrée : {file_path}")

    except Exception as e:
        print("❌ Erreur :", e)

    finally:
        driver.quit()

    return file_path
