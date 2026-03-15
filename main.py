import os
import json
import time
import pandas as pd
from groq import Groq
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError("Erreur : La cle GROQ_API_KEY est introuvable. Verifiez le fichier .env.")

# Initialisation du client API Groq
client = Groq(api_key=API_KEY)

def analyser_review(review_text, max_retries=3):
    """
    Interroge l'API Groq (modele Llama 3) pour faire une analyse de sentiment.
    Retourne un tuple (Sentiment, Mot_cle).
    """
    prompt = f"""
    Tu es un analyste de donnees specialise dans les jeux video.
    Analyse l'avis de joueur suivant et retourne UNIQUEMENT un objet JSON strict avec deux cles :
    - "sentiment": "Positif", "Negatif" ou "Neutre"
    - "mot_cle": Le sujet principal de l'avis en un mot (ex: Equilibrage, Graphismes, Serveurs, etc.)

    Avis du joueur : "{review_text}"
    """
    
    for tentative in range(max_retries):
        try:
            # Appel a l'API avec le modele Llama 3 (8 milliards de parametres)
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant",
                response_format={"type": "json_object"},
                temperature=0.2
            )
            
            texte_brut = response.choices[0].message.content
            resultat = json.loads(texte_brut)
            
            return resultat.get("sentiment", "Inconnu"), resultat.get("mot_cle", "Inconnu")
            
        except Exception as e:
            print(f"    [Avertissement] Tentative {tentative + 1}/{max_retries} echouee : {e}")
            if tentative < max_retries - 1:
                time.sleep(2)
            else:
                return "ERROR", "ERROR"

def main():
    input_file = "donnees.csv"
    output_file = "resultats_analyse.csv"

    print(f"Chargement du fichier source : {input_file}")
    
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Erreur fatale : Le fichier {input_file} est introuvable.")
        return

    if "Avis" not in df.columns:
        print("Erreur fatale : Le fichier CSV doit contenir une colonne 'Avis'.")
        return

    print("Demarrage de l'analyse IA des retours joueurs via Groq...")
    sentiments = []
    mots_cles = []

    for index, row in df.iterrows():
        print(f"Traitement de la ligne {index + 1}/{len(df)}")
        sentiment, mot_cle = analyser_review(row["Avis"])
        
        sentiments.append(sentiment)
        mots_cles.append(mot_cle)
        
        # Courte pause par securite, bien que Groq soit tres permissif
        time.sleep(1) 

    df["Sentiment"] = sentiments
    df["Mot_Cle"] = mots_cles

    print(f"Ecriture des resultats dans : {output_file}")
    df.to_csv(output_file, index=False)
    print("Pipeline d'analyse termine avec succes.")

if __name__ == "__main__":
    main()