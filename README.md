# Word Ladder

Jeu éducatif de transformation de mots en français, anglais et espagnol. À chaque tour, change une lettre pour former un mot valide. Joue seul contre l’ordinateur ou en duel local à deux joueurs sur le même appareil.

Le projet est conçu pour une démonstration locale. Il ne propose pas de duel en ligne ni de déploiement public configuré.

## Fonctionnalités

- Parcours de jeu en plusieurs étapes, trois langues et trois niveaux.
- Clavier tactile et saisie au clavier physique.
- Comptes facultatifs avec sessions serveur; le mode invité est disponible.
- Classement local des parties terminées.
- API FastAPI, SQLite et Redis facultatif pour l’état temporaire des parties.
- Échéances de tour calculées par le serveur et compte à rebours synchronisé dans l’interface.

Les comptes ne demandent pas d’adresse e-mail. La récupération d’un mot de passe oublié n’est donc pas disponible. N’utilise pas cette démo pour des données personnelles ou des mots de passe réutilisés.

## Prérequis

- Python 3.12
- Node.js 22
- Redis est facultatif en lancement direct; Docker Compose le fournit pour une configuration locale complète.

## Démarrage avec Docker Compose

Depuis la racine du dépôt :

```bash
docker compose up --build
```

Le backend est disponible sur `http://127.0.0.1:8000` et l’interface de l’API sur `http://127.0.0.1:8000/docs`. SQLite et Redis utilisent des volumes nommés pour conserver leurs données lorsque les conteneurs sont recréés. Les ports sont liés à l’interface locale de la machine.

## Démarrage depuis les sources

Dans un premier terminal, depuis la racine :

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
Set-Location backend
python -m pip install -r requirements.txt
Copy-Item .env.example .env
$env:WL_ENVIRONMENT = "development"
python -m uvicorn app.main:app --reload --port 8000
```

Dans un second terminal :

```powershell
Set-Location frontend
npm ci
npm run dev
```

Vite sert l’application sur `http://localhost:5173` et relaie les appels API vers le backend local.

## Vérification

Depuis `backend/` :

```bash
python -m pytest -q
```

Depuis `frontend/` :

```bash
npm test
npm run build
```

La CI exécute les tests du backend, les tests des composants frontend et le build de production.

## Stockage et confidentialité

La base locale contient les comptes facultatifs et les résultats de parties terminées. Les mots de passe sont hachés; les sessions sont stockées côté serveur. Les données locales ne sont pas chiffrées et le classement associe le pseudo aux résultats. La route `GET /` ne publie que les métadonnées du projet et les chemins de documentation/santé.
