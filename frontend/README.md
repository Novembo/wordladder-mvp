# Word Ladder — Frontend

Interface web développée avec **Vue 3 (Composition API / `<script setup>`)**, **Vite**, **Vue Router 4** et **Pinia**.

🎮 **Démo en ligne :** [https://novembo.github.io/wordladder-mvp/](https://novembo.github.io/wordladder-mvp/)  
Documentation générale et backend : [README principal](../README.md).

---

## Particularités Architecturales

### 1. Fonctionnement Dual (Connecté ou 100% Autonome)
Le frontend est conçu pour être résilient et fonctionnel même sans serveur :
- **Mode Connecté (API FastAPI)** : Lorsque le backend local ou distant est joignable, les parties, sessions et classements sont synchronisés via l'API.
- **Mode Autonome Direct (Client-Side)** : Si le backend est éteint, inaccessible ou en veille (ex. hébergement statique GitHub Pages sans serveur payant), le store Pinia bascule automatiquement et instantanément sur le moteur interne (`src/services/localEngine.js`). Les dictionnaires (`public/packs/*.json`) sont chargés de façon statique et les scores sont conservés dans `localStorage`.

### 2. Accessibilité & Ergonomie Mobile
- Clavier virtuel tactile responsive adapté aux petits écrans et disposition ergonomique.
- Support natif complet du clavier physique.
- Design responsive avec CSS moderne (variables, contrastes conformes WCAG, animations fluides).

---

## Prérequis

- **Node.js 22**
- Backend FastAPI (optionnel pour jouer en mode local connecté, inutile en mode autonome).

---

## Commandes

Depuis le dossier `frontend/` :

```bash
# Installation des dépendances
npm ci

# Serveur de développement avec HMR
npm run dev

# Exécution de la suite de tests (Vitest + JSDOM)
npm test

# Build de production (assets minifiés dans dist/)
npm run build

# Prévisualisation du build de production
npm run preview
```

---

## Structure du Code

- `public/packs/` : Dictionnaires multilingues JSON précalculés (graphes d'adjacence et niveaux de difficulté pour `fr`, `en`, `es`).
- `src/views/` : Vues principales (Accueil, Assistant de configuration `SetupWizardView`, Arène de jeu `GameView`, Écran de fin `ResultView`, Classement `LeaderboardView`).
- `src/components/` : Composants UI réutilisables (clavier virtuel `Keyboard`, compte à rebours circulaire SVG `Timer`, chaîne de mots `WordChain`, tableau des scores `ScoreBoard`, indices `HintBubble`).
- `src/stores/` : Stores Pinia réactifs (`game.js` pour la logique de partie et le fallback, `auth.js` pour la gestion des sessions et préférences).
- `src/services/` : Moteur de jeu autonome côté client (`localEngine.js`) avec validation des règles, IA du robot et indices sémantiques.
- `vite.config.js` : Configuration du bundling, de la base URL pour GitHub Actions et du proxy de développement vers l'API (`/v1` et `/health`).

---

## Déploiement

Le frontend est automatiquement compilé et déployé sur **GitHub Pages** via le workflow GitHub Actions `.github/workflows/deploy-pages.yml` à chaque commit sur `main`. Les dictionnaires statiques sont copiés dans `dist/packs/` lors du build.
