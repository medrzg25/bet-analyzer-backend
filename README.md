# Bet‑Analyzer Backend (Mock)

Ce dépôt contient un service API FastAPI simple qui expose des
endpoints pour le prototype "Bet‑Analyzer". Il fournit des données
d'exemple (mock) permettant de développer et tester une interface
d'analyse de paris hippiques sans avoir à configurer une base de
données ou un scraper.

## Contenu

- `main.py` – application FastAPI avec trois endpoints :
  - `GET /api/programme` : liste des courses du jour et des chevaux les mieux notés.
  - `GET /api/valuebets` : agrégation des chevaux ayant le meilleur potentiel (value edge).
  - `GET /api/course/{course_id}` : détails et classement d'une course spécifique.
- `requirements.txt` – dépendances Python requises.
- `.env.example` – exemple de variables d'environnement (CORS et autres options).

## Lancement local

Assurez‑vous d'avoir installé Python 3.9+ puis installez les dépendances :

```sh
pip install -r requirements.txt
```

Lancez ensuite le serveur avec Uvicorn :

```sh
uvicorn main:app --host 0.0.0.0 --port 8000
```

Le serveur sera accessible sur http://localhost:8000/ et la documentation
interactive (Swagger UI) sur http://localhost:8000/docs.

## Déploiement

Pour un déploiement sur un service comme Railway ou Render :

1. Créez un dépôt Git et poussez ces fichiers.
2. Configurez votre service afin de détecter automatiquement l'environnement
   Python et installez `pip install -r requirements.txt`.
3. Indiquez la commande de démarrage suivante :

   ```sh
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

4. Ajoutez la variable d'environnement `ORIGIN_FRONTEND` pointant vers
   l'URL de votre front‑end (par exemple, `https://bet-analyzer.fr`).

Ce backend mock fournit des réponses en français et peut être étendu
facilement pour lire des données réelles et calculer des probabilités
dynamiques.