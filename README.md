# Word Ladder — Le Jeu de Vocabulaire Éducatif

Jeu éducatif de transformation de mots en français, anglais et espagnol. À chaque tour, change exactement une lettre pour former un mot valide du dictionnaire. Joue seul contre le robot ou en duel local (pass & play) à deux joueurs sur le même appareil.

🎮 **Jouer en ligne immédiatement (gratuit, sans inscription) :**  
👉 **[https://novembo.github.io/wordladder-mvp/](https://novembo.github.io/wordladder-mvp/)**

---

## Architecture & Déploiement 100% Gratuit

Le projet est conçu avec une architecture résiliente à double mode, pensée pour fonctionner sans aucun abonnement payant :

1. **Mode Autonome / Client-Side (GitHub Pages) :**
   - Le navigateur embarque un moteur de jeu complet (`localEngine.js`) et les dictionnaires précalculés (`packs/fr.json`, `en.json`, `es.json`).
   - Le jeu tourne à 100% dans le navigateur de l'utilisateur, avec validation des mots, IA solo adaptative, chronomètre, indices sémantiques et persistance des scores dans `localStorage`.
   - **Coût d'hébergement : 0 €** (aucun serveur nécessaire pour jouer).

2. **Mode Backend API (FastAPI + SQLite / Redis) :**
   - Pour le jeu avec comptes utilisateurs, sessions HttpOnly et classement centralisé.
   - En ligne, le frontend détecte automatiquement la disponibilité du backend : si le serveur est en veille ou éteint (ex. cold start Render free-tier), le jeu bascule **instantanément et de manière transparente** en mode autonome direct.
   - Un workflow GitHub Actions (`keep-alive.yml`) peut pinguer l'API toutes les 14 minutes pour maintenir le serveur éveillé sur les plateformes gratuites.

---

## Fonctionnalités

- **Parcours interactif** : Assistant de configuration en 3 étapes (Mode Solo/Duo, Langue FR/EN/ES, Niveau Basique/Intermédiaire/Avancé).
- **Moteur de jeu complet** :
  - Dictionnaires graphes d'adjacence précalculés (plus de 4 000 mots par langue).
  - IA pour le mode Solo qui s'adapte au niveau choisi.
  - Système de 3 manches, 3 cœurs d'énergie (vies) par manche et calcul de score.
  - Chronomètre adaptatif (+10s après un temps écoulé, -5s après un coup fatal / impasse).
  - Système d'indices pédagogiques (définitions et repérage de la lettre à changer).
- **Double saisie** : Clavier virtuel tactile responsive ou saisie directe au clavier physique.
- **Comptes et sessions** : Mode invité par défaut (immédiat), comptes facultatifs sans e-mail requis.
- **Classement** : Tableau des scores avec bascule automatique entre API centrale et stockage local navigateur.

---

## Prérequis pour le développement local

- **Python 3.12+**
- **Node.js 22+**
- **Docker & Docker Compose** (facultatif, pour exécuter l'environnement complet avec Redis)

---

## Démarrage rapide avec Docker Compose

Depuis la racine du projet :

```bash
docker compose up --build
```

- Frontend : `http://localhost:5173`
- Backend API : `http://127.0.0.1:8000`
- Documentation interactive OpenAPI (Swagger) : `http://127.0.0.1:8000/docs`

---

## Démarrage depuis les sources

### 1. Backend (FastAPI)

Dans un premier terminal :

```powershell
# Créer et activer l'environnement virtuel
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1

# Installer les dépendances
python -m pip install -r backend/requirements.txt

# Lancer le serveur de développement
Set-Location backend
Copy-Item .env.example .env -ErrorAction SilentlyContinue
$env:WL_ENVIRONMENT = "development"
python manage.py runserver
```

L'API tourne sur `http://127.0.0.1:8000`.

### 2. Frontend (Vue 3 + Vite)

Dans un second terminal :

```powershell
Set-Location frontend
npm ci
npm run dev
```

L'application est accessible sur `http://localhost:5173` avec proxy automatique vers le backend.

---

## Tests et Qualité

### Tests Backend (Pytest)

Depuis le dossier `backend/` :

```bash
python manage.py test
```
*Ou directement depuis la racine :*
```bash
python -m pytest backend/ -q
```
*Vérifie 18 tests : flux complet des matchs, calcul des échéances, sécurité des cookies, hachage des mots de passe, rate-limiting, reset dev-only et migrations Alembic.*

### Tests Frontend (Vitest)

Depuis le dossier `frontend/` :

```bash
npm test
npm run build
```
*Exécute les tests de composants (Timer, Clavier), la gestion des erreurs API du store Pinia, et la bascule automatique vers le moteur autonome client-side.*

---

## Déploiement

- **Frontend (GitHub Pages)** : Automatisé via le workflow `.github/workflows/deploy-pages.yml` lors de chaque push sur la branche `main`.
- **Backend (Render Free)** : Configuré via `render.yaml`. Le workflow `.github/workflows/keep-alive.yml` prévient l'endormissement de l'instance gratuite.

---

## Confidentialité & Sécurité

- Aucun e-mail n'est collecté : les comptes ne stockent qu'un pseudo et un mot de passe haché (Argon2 / pwdlib).
- Protection contre les attaques par force brute (rate limiting par IP et pseudo).
- Cookies de session sécurisés (`HttpOnly`, `SameSite=Lax`, `Secure` hors dev) avec jeton de synchronisation anti-CSRF.
- La route racine `GET /` ne diffuse aucune donnée personnelle ni adresse e-mail.
