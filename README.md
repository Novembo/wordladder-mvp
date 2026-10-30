# 🪜 Word Ladder — Jeu Éducatif & Pédagogique (MVP Complet)

Word Ladder est une application EdTech moderne, engageante et performante conçue pour l'apprentissage et l'enrichissement du vocabulaire en plusieurs langues (**Français 🇫🇷**, **Anglais 🇬🇧**, **Espagnol 🇪🇸**).

Le principe : transformer un mot de départ en changeant **exactement une lettre à chaque tour** pour former un mot valide du dictionnaire, contre l'ordinateur ou en duel local deux joueurs.

---

## 🚀 Architecture Technique

| Couche | Technologies & Rôles |
|---|---|
| **Frontend** | **Vite 6** + **Vue 3** (Composition API) + **Pinia** + **Vue Router** |
| **Design System** | Dark mode moderne, Glassmorphism, animations fluides, typographies *Outfit* & *JetBrains Mono* |
| **Backend** | **FastAPI** + **SQLAlchemy 2.0 (Async)** + **Alembic** |
| **Base de Données** | **SQLite** (via `aiosqlite`) pour le développement et la persistance locale |
| **Cache & Sessions** | **Redis** (avec repli transparent en mémoire si Redis n'est pas démarré) + msgpack |
| **Temps Réel** | Endpoints REST v1 + **WebSockets** (`/ws/matches/{id}`) |
| **Tests** | **pytest** + `pytest-asyncio` + `httpx` (couverture unitaire & API) |
| **Conteneurs** | `docker-compose.yml` (Redis + FastAPI backend) |

---

## 📂 Structure du Projet

```text
wordladder-mvp/
├── backend/
│   ├── alembic/                # Migrations de schéma de BDD
│   ├── app/
│   │   ├── config.py           # Configuration pydantic-settings
│   │   ├── database.py         # Moteur async SQLAlchemy
│   │   ├── redis_client.py     # Client Redis avec fallback mémoire automatique
│   │   ├── models.py           # Modèles ORM (Word, GraphEdge, MatchRecord, MoveRecord)
│   │   ├── schemas.py          # Schémas Pydantic (Request / Response)
│   │   ├── core.py             # Moteur de règles du jeu (indépendant, déterministe)
│   │   ├── graph.py            # Construction optimisée du graphe O(N*L)
│   │   ├── main.py             # Application factory FastAPI
│   │   ├── routers/
│   │   │   ├── matches.py      # /v1/matches (création, coups, abandon/timeout)
│   │   │   ├── packs.py        # /v1/packs/{lang} & /v1/levels
│   │   │   ├── leaderboard.py  # /v1/leaderboard
│   │   │   └── ws.py           # /ws/matches/{id} (WebSockets temps réel)
│   │   └── services/
│   │       ├── dictionary.py   # Téléchargement, normalisation des accents, filtrage
│   │       ├── graph_service.py# Construction & mise en cache des graphes (msgpack/Redis)
│   │       └── match_service.py# Orchestration du cycle de vie du match
│   ├── data/
│   │   └── packs/              # Packs JSON pré-générés (en.json, fr.json, es.json)
│   ├── scripts/
│   │   └── download_dicts.py   # Générateur de dictionnaires et de tables BDD
│   ├── tests/                  # Tests unitaires et d'intégration API
│   ├── alembic.ini
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── assets/styles/      # Design system CSS moderne
│   │   ├── components/
│   │   │   ├── WordChain.vue   # Échelle animée avec mise en valeur de la lettre modifiée
│   │   │   ├── Timer.vue       # Compteur circulaire dynamique SVG
│   │   │   ├── Keyboard.vue    # Clavier virtuel tactile & saisie clavier physique
│   │   │   ├── ScoreBoard.vue  # Score en temps réel et manches (Best of 3)
│   │   │   └── LangSelector.vue# Choix de langue et niveau de difficulté
│   │   ├── stores/             # Stores Pinia (game.js, auth.js)
│   │   ├── views/
│   │   │   ├── HomeView.vue    # Menu d'accueil & options de jeu
│   │   │   ├── GameView.vue    # Écran de jeu interactif
│   │   │   ├── ResultView.vue  # Écran de fin de match et trophées
│   │   │   └── LeaderboardView.vue # Classement des records
│   │   ├── App.vue
│   │   └── main.js
│   ├── vite.config.js
│   └── package.json
├── docker-compose.yml
└── plan.md
```

---

## 🛠️ Installation et Démarrage

### 1. Backend (FastAPI)

```bash
cd backend
# Activer l'environnement virtuel Python
# Sur Windows :
..\.venv\Scripts\activate
# Installer les dépendances si nécessaire
pip install -r requirements.txt

# Générer les dictionnaires et initialiser la base (optionnel si déjà fait)
python scripts/download_dicts.py

# Lancer le serveur backend
uvicorn app.main:app --reload --port 8000
```
L'API est alors disponible sur `http://localhost:8000` et la documentation interactive sur `http://localhost:8000/docs`.

### 2. Frontend (Vite + Vue 3)

```bash
cd frontend
# Installer les dépendances
npm install

# Démarrer le serveur de développement Vite
npm run dev
```
L'application web s'ouvre sur `http://localhost:5173`. Le proxy Vite redirige automatiquement les appels `/v1` vers le backend FastAPI.

### 3. Exécution des Tests

```bash
cd backend
pytest tests
```

### 4. Déploiement avec Docker Compose

```bash
docker compose up --build
```

---

## 🎯 Fonctionnalités Pédagogiques EdTech

- **Visualisation phonologique & orthographique** : Sur chaque échelon de la chaîne de mots (`WordChain.vue`), la lettre modifiée par rapport au mot précédent est automatiquement surlignée et animée.
- **Support multilingue** : Dictionnaires intégrés avec normalisation automatique des accents et diacritiques (Français, Anglais, Espagnol).
- **Adaptation au niveau de l'apprenant** :
  - **Débutant (60s)** : Mots courts (3-4 lettres).
  - **Intermédiaire (40s)** : Mots de 5 lettres.
  - **Avancé (20s)** : Mots de 6 à 8 lettres.
- **Double accessibilité de saisie** : Clavier virtuel tactile responsive (pour tablettes et smartphones scolaires) et support direct du clavier physique azerty/qwerty pour ordinateurs de bureau.
- **IA pédagogique** : En mode Solo, l'ordinateur adapte sa stratégie (de coups basiques à coups anticipés) selon le niveau choisi.
- **Résilience hors-ligne / Réseau faible** : Fallback mémoire automatique si Redis est indisponible, et possibilité de téléchargement de pack JSON client.

## Licence

Ce projet est distribué sous licence [MIT](LICENSE).
