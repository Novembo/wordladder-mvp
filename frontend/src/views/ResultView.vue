<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useGameStore } from '@/stores/game'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const game = useGameStore()
const auth = useAuthStore()

const isP0Winner = computed(() => game.winner === 0)
const isP1Winner = computed(() => game.winner === 1)

const title = computed(() => {
  if (game.winner === null) return 'Match Nul !'
  if (game.mode === 'solo') {
    return isP0Winner.value ? '🎉 Victoire !' : '🤖 L\'ordinateur l\'emporte !'
  }
  return isP0Winner.value ? `🏆 Victoire de ${auth.username} !` : '🏆 Victoire de Joueur 2 !'
})

const subtitle = computed(() => {
  if (game.mode === 'solo' && isP0Winner.value) {
    return 'Excellente maîtrise du vocabulaire et de l’enchaînement de lettres !'
  }
  if (game.mode === 'solo') {
    return 'Belle tentative ! Entraîne-toi pour anticiper les coups de l\'adversaire.'
  }
  return 'Un duel de vocabulaire intense et instructif.'
})

async function handleReplay() {
  try {
    await game.createMatch(game.lang, game.level, game.mode)
    router.push('/game')
  } catch (err) {
    console.error('Replay failed:', err)
    router.push('/')
  }
}

function handleGoHome() {
  game.reset()
  router.push('/')
}
</script>

<template>
  <div class="result-view container">
    <div class="result-card glass-panel animate-pop">
      <div class="trophy-icon">
        <span v-if="isP0Winner">🏆</span>
        <span v-else-if="game.mode === 'solo'">🤖</span>
        <span v-else>⚔️</span>
      </div>

      <h1 class="result-title">{{ title }}</h1>
      <p class="result-subtitle">{{ subtitle }}</p>

      <!-- Score display -->
      <div class="final-score-box">
        <div class="score-player">
          <span class="score-name">{{ auth.username }}</span>
          <span class="score-val" :class="{ 'score-win': isP0Winner }">{{ game.scores[0] }}</span>
        </div>

        <div class="score-divider">-</div>

        <div class="score-player">
          <span class="score-name">{{ game.mode === 'solo' ? 'IA' : 'Joueur 2' }}</span>
          <span class="score-val" :class="{ 'score-win': isP1Winner }">{{ game.scores[1] }}</span>
        </div>
      </div>

      <!-- Stats Grid -->
      <div class="stats-grid">
        <div class="stat-item">
          <span class="stat-label">Langue</span>
          <span class="stat-value">{{ game.lang.toUpperCase() }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">Difficulté</span>
          <span class="stat-value capitalize">{{ game.level }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">Mots joués</span>
          <span class="stat-value">{{ game.usedCount }}</span>
        </div>
      </div>

      <!-- Actions -->
      <div class="result-actions">
        <button type="button" class="btn btn-primary pulse-glow" @click="handleReplay">
          Rejouer 🔄
        </button>
        <router-link to="/leaderboard" class="btn btn-secondary">
          Classement 🏅
        </router-link>
        <button type="button" class="btn btn-secondary" @click="handleGoHome">
          Menu Principal 🏠
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.result-view {
  min-height: 85vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.result-card {
  max-width: 520px;
  width: 100%;
  padding: 2.5rem 2rem;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
}

.trophy-icon {
  font-size: 3.5rem;
  animation: bounce 1s infinite alternate;
}

@keyframes bounce {
  from { transform: translateY(0); }
  to { transform: translateY(-8px); }
}

.result-title {
  font-size: 2.2rem;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.result-subtitle {
  color: var(--text-muted);
  font-size: 1rem;
  line-height: 1.5;
  max-width: 420px;
}

.final-score-box {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2rem;
  background: rgba(15, 23, 42, 0.7);
  padding: 1rem 2rem;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
  width: 100%;
  max-width: 320px;
}

.score-player {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.score-name {
  font-size: 0.85rem;
  color: var(--text-dim);
  font-weight: 600;
}

.score-val {
  font-size: 2.2rem;
  font-weight: 800;
  font-family: var(--font-mono);
  color: var(--text-main);
}

.score-val.score-win {
  color: var(--accent-success);
}

.score-divider {
  font-size: 1.8rem;
  color: var(--text-dim);
  font-weight: 700;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  width: 100%;
}

.stat-item {
  background: rgba(30, 41, 59, 0.5);
  padding: 0.75rem;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.stat-label {
  font-size: 0.75rem;
  color: var(--text-dim);
  text-transform: uppercase;
}

.stat-value {
  font-weight: 700;
  font-size: 1.1rem;
  color: var(--text-main);
}

.capitalize {
  text-transform: capitalize;
}

.result-actions {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  width: 100%;
  margin-top: 0.5rem;
}
</style>
