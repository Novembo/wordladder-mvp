<script setup>
const emit = defineEmits(['start'])
</script>

<template>
  <div class="hero-poster glass-panel animate-pop">
    <div class="poster-decorations">
      <span class="bubble bubble-1">A</span>
      <span class="bubble bubble-2">Z</span>
      <span class="bubble bubble-3">E</span>
      <span class="bubble bubble-4">⭐</span>
    </div>

    <div class="poster-badge animate-float">
      <span>🪜 Jeu de Mots Magique</span>
    </div>

    <div class="poster-mascots">
      <div class="mascot-circle bot">🤖</div>
      <div class="sparkle">✨</div>
      <div class="mascot-circle player">🧒</div>
    </div>

    <h1 class="poster-title">
      Prêt pour la grande aventure des mots ?
    </h1>

    <p class="poster-description">
      Transforme les mots comme par magie, <strong>une seule lettre à la fois</strong> !
      Gagne des étoiles, relève les défis et deviens le grand champion du vocabulaire.
    </p>

    <div class="poster-features">
      <div class="feat-item">
        <span class="feat-icon">❤️</span>
        <span class="feat-text">3 cœurs pour explorer</span>
      </div>
      <div class="feat-item">
        <span class="feat-icon">💡</span>
        <span class="feat-text">Indices synonymes</span>
      </div>
      <div class="feat-item">
        <span class="feat-icon">🌍</span>
        <span class="feat-text">3 langues à découvrir</span>
      </div>
    </div>

    <button type="button" class="btn btn-primary btn-cta" @click="emit('start')">
      Commencer l'Aventure ! 🚀
    </button>
  </div>
</template>

<style scoped>
.hero-poster {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 3rem 2rem;
  max-width: 620px;
  width: 100%;
  margin: 0 auto;
  overflow: hidden;
  border-radius: var(--radius-lg);
  border: 2px solid rgba(99, 102, 241, 0.3);
}

.poster-decorations {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.bubble {
  position: absolute;
  font-family: var(--font-mono);
  font-weight: 800;
  color: rgba(255, 255, 255, 0.08);
  font-size: 3rem;
  user-select: none;
}

.bubble-1 { top: 10%; left: 8%; transform: rotate(-15deg); }
.bubble-2 { bottom: 15%; left: 10%; transform: rotate(10deg); color: rgba(99, 102, 241, 0.15); font-size: 3.5rem; }
.bubble-3 { top: 12%; right: 8%; transform: rotate(18deg); }
.bubble-4 { bottom: 18%; right: 10%; font-size: 2.2rem; }

.poster-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(99, 102, 241, 0.2);
  border: 1px solid var(--accent-primary);
  padding: 0.4rem 1.1rem;
  border-radius: var(--radius-full);
  font-weight: 700;
  font-size: 0.95rem;
  color: #c7d2fe;
  margin-bottom: 1.25rem;
}

.poster-mascots {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.25rem;
  margin-bottom: 1.25rem;
}

.mascot-circle {
  width: 72px;
  height: 72px;
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.6rem;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.35);
}

.mascot-circle.bot {
  background: linear-gradient(135deg, #ec4899, #f43f5e);
}

.mascot-circle.player {
  background: linear-gradient(135deg, #06b6d4, #3b82f6);
}

.sparkle {
  font-size: 2rem;
  animation: heartBeat 2s infinite;
}

.poster-title {
  font-size: 2.3rem;
  font-weight: 800;
  line-height: 1.2;
  letter-spacing: -0.02em;
  margin-bottom: 1rem;
  background: linear-gradient(135deg, #ffffff 40%, #a5b4fc 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.poster-description {
  font-size: 1.1rem;
  color: var(--text-muted);
  line-height: 1.6;
  max-width: 480px;
  margin-bottom: 1.75rem;
}

.poster-features {
  display: flex;
  justify-content: center;
  gap: 1.25rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.feat-item {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid var(--border-color);
  padding: 0.4rem 0.85rem;
  border-radius: var(--radius-full);
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-main);
}

.feat-icon {
  font-size: 1.1rem;
}

.btn-cta {
  font-size: 1.25rem;
  padding: 1.1rem 2.8rem;
  border-radius: var(--radius-lg);
}

@media (max-width: 600px) {
  .poster-title {
    font-size: 1.8rem;
  }
  .poster-description {
    font-size: 0.95rem;
  }
}
</style>

