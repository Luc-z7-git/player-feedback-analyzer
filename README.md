# Player Feedback Analyzer - AI Pipeline

## Presentation du projet

L'objectif est d'automatiser l'analyse de retours joueurs (Player Insights) en utilisant l'Intelligence Artificielle generative. Le script lit des avis bruts au format CSV, interroge un modele de langage (LLM) pour extraire le sentiment global (Positif/Negatif/Neutre) ainsi qu'un mot-cle principal, puis exporte les donnees structurees pour une integration future dans un tableau de bord.

## Le parcours technique et l'architecture

Ce projet a ete construit avec une approche iterative, axee sur la resilience et l'adaptabilite technique :

1. **Choix de l'architecture initiale :** Le prototype a d'abord ete developpe en ciblant l'API Google Gemini (modeles Flash 1.5 et 2.0). 
2. **Gestion des contraintes Cloud :** Face aux restrictions regionales strictes (quotas bloques a zero pour les comptes gratuits en Europe) et aux erreurs de type "Rate Limiting" (429) ou "Internal Server Error" (500), j'ai implemente une logique de `retry` et de temporisation dans le code.
3. **Migration et agilite :** Pour garantir la stabilite du pipeline de donnees sans dependre d'un fournisseur cloud restrictif, j'ai pivote vers l'API Groq. Le code a ete mis a jour pour interagir avec le modele open-source `llama-3.1-8b-instant`. Cette transition demontre la modularite du code : la logique d'extraction JSON reste intacte malgre le changement total de l'infrastructure IA sous-jacente.

## Fonctionnalites cles
* **Prompt Engineering avance :** Forcage de l'output du modele en un format JSON strict, indispensable pour l'automatisation des donnees.
* **Mecanisme de Retry :** Le script gere de maniere autonome les echecs de connexion au serveur (jusqu'a 3 tentatives) avant de declarer une erreur, evitant ainsi le crash de l'application.
* **Securite :** Gestion des cles d'API via des variables d'environnement (`dotenv`), garantissant qu'aucun secret n'est expose dans le code source.

## Instructions d'installation

1. Cloner le depot localement.
2. Creer et activer un environnement virtuel (`python -m venv venv`).
3. Installer les dependances requises : `pip install -r requirements.txt`.
4. Dupliquer le fichier `.env.example`, le renommer en `.env` et y inserer votre cle API Groq.
5. Lancer l'analyse : `python main.py`.
