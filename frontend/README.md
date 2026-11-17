# Word Ladder — Frontend

Interface du jeu développée avec Vue 3, Vite, Vue Router et Pinia. Le dépôt parent contient l’API, les instructions pour démarrer les deux services et les détails du projet : [README principal](../README.md).

## Prérequis

- Node.js 22 (version utilisée par le workflow CI).
- Le backend FastAPI local, nécessaire aux fonctionnalités qui utilisent l’API.

## Démarrer

Depuis ce dossier :

```bash
npm ci
npm run dev
```

Ouvre `http://localhost:5173`. Le proxy Vite transmet `/v1` et `/health` à `http://127.0.0.1:8000`; démarre donc aussi le backend selon les instructions du [README principal](../README.md).

## Vérifier et construire

```bash
npm run build
npm run preview
```

`npm test` exécute les tests de composants avec Vitest et Vue Test Utils. `npm run build` produit les fichiers statiques de production dans `dist/`. Aucun déploiement web n’est configuré.

## Organisation

- `src/views/` : accueil, configuration, jeu, résultats et classement.
- `src/components/` : éléments réutilisables, dont le clavier, le chrono et la chaîne de mots.
- `src/stores/` : état Pinia du jeu et de l’authentification.
- `vite.config.js` : alias `@` et proxy de développement vers l’API.
- `src/components/Timer.vue` : compte à rebours synchronisé sur l’échéance UTC renvoyée par le backend.

Les comptes sont facultatifs; le mode invité reste disponible. L’authentification utilise un cookie HttpOnly et une protection CSRF. Aucun e-mail n’est demandé, donc aucun parcours de récupération de mot de passe n’est prévu.

Le duel est local, sur le même écran. L’API ne fournit pas de synchronisation multijoueur WebSocket.
