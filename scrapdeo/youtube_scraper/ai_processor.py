# ai_processor.py
import os
import google.generativeai as genai  # Import correct (vérifie avec pip show google-generativeai)

# Configuration globale (une seule fois)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_image_with_gemini(image_path: str) -> str:
    # Modèle actuel : Gemini 2.5 Flash (stable, multimodal, rapide)
    model = genai.GenerativeModel("gemini-2.5-flash")

    # Upload automatique de l'image (Gemini gère tout, pas de base64)
    image_file = genai.upload_file(path=image_path, mime_type="image/png")

    # Prompt optimisé pour un JSON propre (ajoute "retourne UNIQUEMENT du JSON valide")
    prompt = (
        "Tu analyses une capture d'écran de résultats YouTube pour un anime. "
        "Extrait les infos de chacune des images,videos (pas les pubs ou suggestions). "
        "Retourne **UNIQUEMENT** un JSON valide, sans texte supplémentaire, avec exactement ces clés :\n"
        "{\n"
        '  "titre": "titre complet de la vidéo",\n'
        '  "chaine": "nom exact de la chaîne YouTube",\n'
        '  "date_publication": "date relative ou absolue (ex: \"il y a 2 jours\" ou \"15 oct. 2025\")",\n'
        '  "vues": "nombre de vues (ex: \"1,2 M\" ou \"456 vues\")",\n'
        '  "description_visuelle": "description courte (2-3 phrases) de la miniature, du style de la vidéo et de la page de résultats"\n'
        "}\n\n"
        "Si une info manque, mets 'Non visible'."
    )

    try:
        response = model.generate_content([prompt, image_file])
        return response.text.strip()  # Retourne le texte nettoyé
    except Exception as e:
        return f"Erreur Gemini : {str(e)}"  # Gestion basique des erreurs