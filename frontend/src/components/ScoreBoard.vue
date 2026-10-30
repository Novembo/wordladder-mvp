<script setup>
import { computed } from 'vue'
import { useGameStore } from '@/stores/game'

const game = useGameStore()

const p1Name = computed(() => 'Joueur 1')
const p2Name = computed(() => game.mode === 'solo' ? 'Robot Antigravity' : 'Joueur 2')
</script>

<template>
  <div class="scoreboard-container glass-panel">
    <div class="part-badge">
      <span class="part-icon">🎯</span>
      <span class="part-text">Manche {{ game.part }} / 3</span>
    </div>

    <div class="scores-wrapper">
      <!-- Player 1 Card -->
      <div class="player-card" :class="{ active: game.toMove === 0 && !game.finished }">
        <div class="player-avatar p1">P1</div>
        <div class="player-info">
          <div class="player-name">{{ p1Name }}</div>
          <div class="player-score">{{ game.scores[0] }}</div>
          <div class="lives-row" title="3 cœurs d'énergie">
            <span
              v-for="i in 3"
              :key="i"
              class="heart-icon"
              :class="{ full: i <= (game.lives?.[0] ?? 3), lost: i > (game.lives?.[0] ?? 3) }"
            >
              {{ i <= (game.lives?.[0] ?? 3) ? '❤️' : '🤍' }}
            </span>
          </div>
        </div>
      </div>

      <div class="vs-badge">VS</div>

      <!-- Player 2 / Bot Card -->
      <div class="player-card" :class="{ active: game.toMove === 1 && !game.finished }">
        <div class="player-avatar" :class="game.mode === 'solo' ? 'ai' : 'p2'">
          {{ game.mode === 'solo' ? '🤖' : 'P2' }}
        </div>
        <div class="player-info">
          <div class="player-name">{{ p2Name }}</div>
          <div class="player-score">{{ game.scores[1] }}</div>
          <div class="lives-row" title="3 cœurs d'énergie">
            <span
              v-for="i in 3"
              :key="i"
              class="heart-icon"
              :class="{ full: i <= (game.lives?.[1] ?? 3), lost: i > (game.lives?.[1] ?? 3) }"
            >
              {{ i <= (game.lives?.[1] ?? 3) ? '❤️' : '🤍' }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.scoreboard-container {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 1rem 1.25rem;
  margin-bottom: 1.25rem;
}

.part-badge {
  display: inline-flex;
  align-items: center;
  align-self: center;
  gap: 0.4rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-color);
  padding: 0.35rem 0.85rem;
  border-radius: var(--radius-full);
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--accent-secondary);
}

.scores-wrapper {
  display: flex;
  align-items: center;
  justify-content: space-around;
  gap: 1rem;
}

.player-card {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.6rem 0.95rem;
  border-radius: var(--radius-md);
  border: 1.5px solid transparent;
  transition: all 0.3s ease;
}

.player-card.active {
  background: rgba(99, 102, 241, 0.15);
  border-color: var(--accent-primary);
  box-shadow: 0 0 15px rgba(99, 102, 241, 0.25);
}

.player-avatar {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1rem;
  flex-shrink: 0;
}

.player-avatar.p1 {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: #fff;
}

.player-avatar.p2 {
  background: linear-gradient(135deg, #06b6d4, #3b82f6);
  color: #fff;
}

.player-avatar.ai {
  background: linear-gradient(135deg, #ec4899, #f43f5e);
  font-size: 1.3rem;
}

.player-info {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.player-name {
  font-size: 0.85rem;
  color: var(--text-muted);
  font-weight: 600;
}

.player-score {
  font-size: 1.45rem;
  font-weight: 800;
  color: var(--text-main);
  line-height: 1.1;
}

.lives-row {
  display: flex;
  gap: 0.25rem;
  margin-top: 0.2rem;
}

.heart-icon {
  font-size: 0.95rem;
  transition: transform 0.2s ease, opacity 0.2s ease;
}

.heart-icon.full {
  opacity: 1;
  filter: drop-shadow(0 0 4px rgba(244, 63, 94, 0.5));
}

.heart-icon.lost {
  opacity: 0.35;
  filter: grayscale(1);
}

.vs-badge {
  font-size: 0.8rem;
  font-weight: 800;
  letter-spacing: 0.05em;
  color: var(--text-dim);
}
</style>
