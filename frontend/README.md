# 🎨 Word Ladder Frontend (Vite + Vue 3)

Ce dossier contient l'interface utilisateur interactive et éducative du jeu Word Ladder.

## 📦 Gestionnaire de paquets & dépendances

Contrairement au backend qui utilise Python et `pip` (`requirements.txt`), le frontend est développé en **JavaScript / Vue 3** et s'appuie sur l'écosystème **Node.js** :
- Le fichier officiel qui déclare les dépendances est **[`package.json`](./package.json)**.
- Un fichier indicatif **[`requirements.txt`](./requirements.txt)** a également été ajouté pour lister les technologies employées.

## 🚀 Démarrer le Frontend

1. **Installer les dépendances (déjà fait si le dossier `node_modules` existe)** :
   ```bash
   npm install
   ```

2. **Lancer le serveur de développement Vite** :
   ```bash
   npm run dev
   ```
   L'application sera immédiatement accessible sur : **`http://localhost:5173`**

3. **Compiler pour la production** :
   ```bash
   npm run build
   ```

## 🧩 Architecture des composants

- **`src/views/HomeView.vue`** : Choix de langue (FR, EN, ES), difficulté (Débutant, Intermédiaire, Expert) et mode (Solo vs IA ou Duo Pass & Play).
- **`src/views/GameView.vue`** : Écran principal avec l'échelle de mots en cascade, le compte à rebours dynamique, les cases de saisie et le clavier virtuel interactif.
- **`src/views/ResultView.vue`** : Écran de fin de partie avec podium, scores détaillés et bouton Rejouer.
- **`src/views/LeaderboardView.vue`** : Tableau d'honneur et classement mondial des meilleurs scores.
- **`src/components/WordChain.vue`** : Algorithme visuel mettant en évidence la lettre modifiée à chaque étape.
- **`src/components/Timer.vue`** : Compteur circulaire SVG fluide et dynamique.
- **`src/components/Keyboard.vue`** : Clavier tactile virtuel responsive et compatible clavier physique.
- **`src/stores/game.js`** : Store Pinia gérant l'état du match et les échanges avec l'API FastAPI.

