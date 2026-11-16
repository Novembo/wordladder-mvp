# 🪜 Word Ladder — Jeu Éducatif & Pédagogique (MVP Complet)

[![CI](https://github.com/Novembo/wordladder-mvp/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/Novembo/wordladder-mvp/actions/workflows/ci.yml)

Word Ladder est une application EdTech moderne, engageante et performante conçue pour l'apprentissage et l'enrichissement du vocabulaire en plusieurs langues (**Français 🇫🇷**, **Anglais 🇬🇧**, **Espagnol 🇪🇸**).

Le principe : transformer un mot de départ en changeant **exactement une lettre à chaque tour** pour former un mot valide du dictionnaire, contre l'ordinateur ou en duel local deux joueurs.

> **Statut :** projet exécutable localement; aucune démo publique ni aucun déploiement automatique n’est configuré. Le workflow CI teste le backend et construit le frontend.

---

## 🚀 Architecture Technique

| Couche | Technologies & Rôles |
|---|---|
| **Frontend** | **Vite 6** + **Vue 3** (Composition API) + **Pinia** + **Vue Router** |
| **Design System** | Dark mode moderne, Glassmorphism, animations fluides, typographies *Outfit* & *JetBrains Mono* |
| **Backend** | **FastAPI** + **SQLAlchemy 2.0 (Async)** + **Alembic** |
| **Base de Données** | **SQLite** (via `aiosqlite`) pour le développement et la persistance locale |
| **Cache** | **Redis**; repli en mémoire dans le processus si Redis est indisponible + msgpack |
| **Sessions utilisateur** | Sessions serveur révocables stockées en base de données; cookie HttpOnly côté navigateur |
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
│   │   │   ├── auth.py         # Comptes, sessions HttpOnly et protections CSRF
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

## 🛠️ Installation et démarrage

Prérequis : Python 3.12 et Node.js 22 (versions utilisées par la CI). Redis et Docker Compose sont facultatifs pour un démarrage simple.

### 1. Backend (FastAPI)

Depuis la racine du dépôt, sous Windows PowerShell :

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
Set-Location backend
python -m pip install -r requirements.txt
Copy-Item .env.example .env
$env:WL_ENVIRONMENT = "development"
python -m uvicorn app.main:app --reload --port 8000
```

L'API est disponible sur `http://localhost:8000`; la documentation interactive est sur `http://localhost:8000/docs`.

Sous Bash, depuis la racine du dépôt :

```bash
python3.12 -m venv .venv
source .venv/bin/activate
cd backend
python -m pip install -r requirements.txt
cp .env.example .env
WL_ENVIRONMENT=development python -m uvicorn app.main:app --reload --port 8000
```

### 2. Frontend (Vite + Vue 3)

Dans un second terminal, depuis la racine du dépôt :

```bash
cd frontend
npm ci
npm run dev
```

L'application web s'ouvre sur `http://localhost:5173`. Le proxy Vite redirige les appels `/v1` et `/health` vers le backend local.

### 3. Tests et CI

Depuis `backend/`, exécute `python -m pytest -q`. Le workflow GitHub Actions lance les tests du backend et construit le frontend à chaque pull request et push sur `main`; il ne déploie pas l’application.

### 4. Services locaux avec Docker Compose

```bash
docker compose up --build
```

Compose démarre le backend et Redis pour le développement local; il ne constitue pas un déploiement de production.

---

## 🎯 Fonctionnalités Pédagogiques EdTech

- **Visualisation phonologique & orthographique** : Sur chaque échelon de la chaîne de mots (`WordChain.vue`), la lettre modifiée par rapport au mot précédent est automatiquement surlignée et animée.
- **Support multilingue** : Dictionnaires intégrés avec normalisation automatique des accents et diacritiques (Français, Anglais, Espagnol).
- **Adaptation au niveau de l'apprenant** :
  - **Débutant (60s)** : Mots courts (3-4 lettres).
  - **Intermédiaire (40s)** : Mots de 5 lettres.
  - **Avancé (20s)** : Mots de 6 à 8 lettres.
- **Double accessibilité de saisie** : Clavier virtuel tactile responsive (pour tablettes et smartphones scolaires) et support direct du clavier physique azerty/qwerty pour ordinateurs de bureau.
- **Adversaire algorithmique** : En mode Solo, l'ordinateur adapte ses coups au niveau choisi; il ne s'agit pas d'un service d'IA générative.
- **Packs de mots** : L'API expose un endpoint de téléchargement JSON par langue. Le repli Redis en mémoire est local à un processus et ne remplace ni une base persistante ni un mode hors ligne complet du frontend.
- **Défi adaptatif** : Le temps accordé évolue entre les manches (+10 s après une perte au chrono, -5 s après un cul-de-sac réussi) sans modifier la longueur constante des mots.
- **Maintenance locale** : Le bouton de réinitialisation efface uniquement les parties archivées et leurs coups; il est désactivé par défaut hors développement.
- **Comptes facultatifs** : création d’un pseudo (3–20 lettres/chiffres/underscores) et mot de passe (8–128 caractères). Les mots de passe sont hachés avec Argon2; les sessions utilisent des cookies HttpOnly/SameSite et protection CSRF. Les parties invitées restent disponibles. Aucun e-mail n’est demandé : un mot de passe oublié ne peut donc pas être récupéré.

Pour le développement local, définissez `WL_ENVIRONMENT=development` dans `backend/.env` afin d’autoriser le cookie de session non-Secure sur HTTP. Configurez `WL_CORS_ORIGINS` avec les origines exactes du frontend en production (valeur par défaut : `http://localhost:5173` et `http://127.0.0.1:5173`) ainsi qu’une clé aléatoire stable `WL_AUTH_RATE_LIMIT_KEY` d’au moins 32 caractères, partagée entre les instances. Les migrations Alembic sont appliquées automatiquement au démarrage, y compris à une base existante.

## Licence

Ce projet est distribué sous licence [MIT](LICENSE).
