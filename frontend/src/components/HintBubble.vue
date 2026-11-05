<script setup>
import { ref } from 'vue'
import { useGameStore } from '@/stores/game'

const game = useGameStore()
const requesting = ref(false)

async function handleGetHint() {
  if (requesting.value || game.loading) return
  requesting.value = true
  try {
    await game.requestHint()
  } finally {
    requesting.value = false
  }
}

function handleCloseHint() {
  game.clearHint()
}
</script>

<template>
  <div class="hint-container">
    <!-- Trigger Button when no hint is displayed -->
    <div v-if="!game.currentHint" class="hint-trigger-wrap">
      <button
        type="button"
        class="btn-hint pulse-subtle"
        :disabled="requesting || game.loading || !game.isMyTurn"
        @click="handleGetHint"
      >
        <span class="hint-lamp">💡</span>
        <span class="hint-btn-text">
          <span v-if="requesting">Le génie réfléchit...</span>
          <span v-else>Besoin d'un indice magique ?</span>
        </span>
      </button>
    </div>

    <!-- Friendly Pedagogical Hint Bubble -->
    <div v-else class="hint-bubble glass-panel animate-pop">
      <div class="bubble-avatar">
        🧙‍♂️
      </div>

      <div class="bubble-content">
        <div class="bubble-header">
          <span class="bubble-badge">Indice Pédagogique</span>
          <button type="button" class="btn-close-hint" aria-label="Fermer l'indice" @click="handleCloseHint">
            ✕
          </button>
        </div>
        <p class="bubble-text">
          {{ game.currentHint.clue }}
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.hint-container {
  width: 100%;
  margin: 0.75rem 0;
  display: flex;
  justify-content: center;
}

@media (max-width: 600px) {
  .hint-container {
    margin: 0.25rem 0;
  }
}

.hint-trigger-wrap {
  display: flex;
  justify-content: center;
  width: 100%;
}

.btn-hint {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  min-height: 48px;
  background: rgba(251, 191, 36, 0.12);
  border: 1.5px solid rgba(251, 191, 36, 0.4);
  color: #fef08a;
  padding: 0.6rem 1.25rem;
  border-radius: var(--radius-full);
  font-family: var(--font-main);
  font-weight: 700;
  font-size: 0.95rem;
  cursor: pointer;
  box-shadow: 0 4px 0 rgba(180, 83, 9, 0.4);
  transition: var(--motion-interactive);
  user-select: none;
}

.btn-hint:hover:not(:disabled) {
  background: rgba(251, 191, 36, 0.22);
  transform: translateY(-2px);
  box-shadow: 0 6px 0 rgba(180, 83, 9, 0.4);
}

.btn-hint:active:not(:disabled) {
  transform: translateY(3px);
  box-shadow: 0 1px 0 rgba(180, 83, 9, 0.4);
}

.btn-hint:disabled {
  opacity: 0.45;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.hint-lamp {
  font-size: 1.25rem;
}

@keyframes subtlePulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.02); }
}

.pulse-subtle {
  animation: subtlePulse 2.5s infinite ease-in-out;
}

.hint-bubble {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1rem 1.25rem;
  width: 100%;
  background: rgba(30, 27, 75, 0.85);
  border: 1.5px solid rgba(251, 191, 36, 0.4);
  box-shadow: 0 8px 24px rgba(251, 191, 36, 0.15);
  border-radius: var(--radius-md);
  position: relative;
}

.bubble-avatar {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-full);
  background: rgba(251, 191, 36, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.6rem;
  flex-shrink: 0;
}

.bubble-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.bubble-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.bubble-badge {
  font-size: 0.75rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--accent-gold);
}

.btn-close-hint {
  min-width: 44px;
  min-height: 44px;
  background: transparent;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  font-size: 1rem;
  padding: 0.2rem 0.4rem;
  border-radius: var(--radius-sm);
  transition: var(--motion-interactive);
}

.btn-close-hint:hover {
  color: var(--text-main);
  background: rgba(255, 255, 255, 0.1);
}

.bubble-text {
  font-size: 0.95rem;
  line-height: 1.45;
  color: #fef08a;
  font-weight: 600;
}
</style>
