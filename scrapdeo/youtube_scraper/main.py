from capture import capture_for_anime
from ai_processor import analyze_image_with_gemini
import json

ANIME_LIST = [
    "Jujutsu Kaisen",
    "Solo Leveling",
    "Tokyo Ghoul",
    "Bleach",
    "Naruto",
    "Chainsaw Man",
    "One Piece"
]

all_results = {}

for anime in ANIME_LIST:
    print(f"\n--- 📸 Traitement : {anime} ---")

    # 1. Capture YouTube
    image_path = capture_for_anime(anime)

    # 2. Analyse avec Gemini
    ai_result = analyze_image_with_gemini(image_path)

    # 3. Stockage
    all_results[anime] = {
        "image": image_path,
        "analysis": ai_result
    }

# Sauvegarde des résultats
with open("analysis_results.json", "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=4, ensure_ascii=False)

print("\n🎉 Analyse complète terminée ! Résultats dans analysis_results.json")
