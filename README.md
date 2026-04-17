# Projet de fin de TP — Agent LangChain

Petit projet Python pour un agent LangChain avec outils métier, données locales et interfaces de démonstration.

## Prérequis
- Python 3.11 ou supérieur
- Une clé API OpenAI dans `OPENAI_API_KEY`
- Optionnel : une clé Tavily dans `TAVILY_API_KEY`

## Installation
1. Créer un environnement virtuel si besoin
2. Installer les dépendances:

```bash
pip install -r requirements.txt
```

## Configuration
1. Copier le fichier `.env.example` en `.env`
2. Ajouter au minimum :
   - `OPENAI_API_KEY`
3. Optionnel :
   - `TAVILY_API_KEY`
   - `FASTAPI_API_KEY`

## Initialiser la base de données
Le projet utilise SQLite pour les données clients et produits

```bash
python init_db.py
```

Ce script crée `database.db` et remplit les tables avec les données de départ.

## Lancer le projet

### 1. Version terminal
Menu de scénarios pour tester l'agent :

```bash
python main.py
```

### 2. Interface web Streamlit

```bash
streamlit run app.py
```

### 3. API REST

```bash
uvicorn main_api:app --reload
```

Endpoint principal :
- `POST /api/agent/query`

Exemple :

```bash
curl -X POST http://127.0.0.1:8000/api/agent/query \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer change-me' \
  -d '{"query":"Quels sont mes clients VIP ?"}'
```

## Fonctionnement
L'agent peut notamment :
- chercher un client ou un produit dans la base SQLite
- afficher des cours boursiers réels avec `yfinance`
- calculer un portefeuille d'actions
- faire des calculs financiers
- résumer du texte
- répondre via l'interface Streamlit ou l'API REST

## Fichiers utiles
- `main.py` : menu CLI
- `app.py` : interface Streamlit
- `main_api.py` : API REST
- `init_db.py` : création de la base SQLite
- `agent.py` : configuration de l'agent et des outils

## Remarque
Si une clé Tavily n'est pas renseignée, la recherche web n'est pas activée.