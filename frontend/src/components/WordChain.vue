<script setup>
import { computed, nextTick, ref, watch } from 'vue'
import { useGameStore } from '@/stores/game'

const game = useGameStore()
const ladderContainer = ref(null)

// Function to compute differences letter by letter
function getLetterDiff(prevWord, currentWord) {
  if (!prevWord || prevWord.length !== currentWord.length) {
    return currentWord.split('').map(char => ({ char, isChanged: false }))
  }

  return currentWord.split('').map((char, index) => ({
    char,
    isChanged: char !== prevWord[index]
  }))
}

const displayLadder = computed(() => {
  const list = game.wordHistory
  return list.map((item, idx) => {
    const prev = idx > 0 ? list[idx - 1].word : null
    const letters = getLetterDiff(prev, item.word)
    return {
      ...item,
      letters,
      isStart: idx === 0,
      isCurrent: idx === list.length - 1
    }
  })
})

watch(
  () => game.wordHistory.length,
  async () => {
    await nextTick()
    if (ladderContainer.value) {
      ladderContainer.value.scrollTop = ladderContainer.value.scrollHeight
    }
  }
)
</script>

<template>
  <div class="ladder-wrapper glass-panel">
    <div class="ladder-header">
      <span class="ladder-title">Échelle de Mots</span>
      <span class="ladder-count">{{ game.wordHistory.length }} mots joués</span>
    </div>

    <div ref="ladderContainer" class="ladder-scroll">
      <div v-if="displayLadder.length === 0" class="empty-hint">
        En attente du premier mot...
      </div>

      <div
        v-for="(step, idx) in displayLadder"
        :key="idx"
        class="ladder-step"
        :class="{
          'is-current': step.isCurrent,
          'is-start': step.isStart,
          'p0-move': step.player === 0,
          'p1-move': step.player === 1
        }"
      >
        <div class="step-connector" v-if="idx > 0">
          <div class="connector-line"></div>
          <div class="connector-dot"></div>
        </div>

        <div class="step-card">
          <div class="player-tag" v-if="!step.isStart">
            <span v-if="step.player === 0">J1</span>
            <span v-else-if="step.player === 1">{{ game.mode === 'solo' ? 'IA' : 'J2' }}</span>
          </div>
          <div class="player-tag start-tag" v-else>
            Départ
          </div>

          <div class="letters-row">
            <span
              v-for="(l, lIdx) in step.letters"
              :key="lIdx"
              class="letter-tile"
              :class="{ 'changed-letter': l.isChanged }"
            >
              {{ l.char.toUpperCase() }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.ladder-wrapper {
  display: flex;
  flex-direction: column;
  padding: 1rem 1.25rem;
  margin-bottom: 1.25rem;
  max-height: 260px;
}

@media (max-width: 600px) {
  .ladder-wrapper {
    padding: 0.5rem 0.75rem;
    margin-bottom: 0.5rem;
    max-height: 140px;
  }
}

.ladder-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--border-color);
}

.ladder-title {
  font-size: 0.85rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--accent-secondary);
}

.ladder-count {
  font-size: 0.8rem;
  color: var(--text-dim);
}

.ladder-scroll {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  overflow-y: auto;
  padding-right: 0.4rem;
  scroll-behavior: smooth;
}

.ladder-scroll::-webkit-scrollbar {
  width: 5px;
}
.ladder-scroll::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.15);
  border-radius: 4px;
}

.empty-hint {
  text-align: center;
  color: var(--text-dim);
  font-size: 0.9rem;
  padding: 2rem 0;
}

.ladder-step {
  display: flex;
  flex-direction: column;
  position: relative;
  animation: popIn 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.step-connector {
  position: relative;
  height: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.connector-line {
  position: absolute;
  width: 2px;
  height: 100%;
  background: rgba(255, 255, 255, 0.12);
}

.connector-dot {
  width: 6px;
  height: 6px;
  border-radius: var(--radius-full);
  background: var(--accent-primary);
  z-index: 1;
}

.step-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: rgba(18, 24, 38, 0.85);
  border: 1px solid var(--border-color);
  padding: 0.5rem 0.85rem;
  border-radius: var(--radius-md);
  transition: var(--motion-interactive);
}

.ladder-step.is-current .step-card {
  border-color: var(--accent-primary);
  background: rgba(99, 102, 241, 0.12);
  box-shadow: 0 0 15px rgba(99, 102, 241, 0.2);
}

.player-tag {
  font-size: 0.7rem;
  font-weight: 700;
  padding: 0.15rem 0.45rem;
  border-radius: var(--radius-sm);
  background: rgba(255, 255, 255, 0.08);
  color: var(--text-muted);
}

.p0-move .player-tag {
  background: rgba(99, 102, 241, 0.2);
  color: var(--accent-primary);
}

.p1-move .player-tag {
  background: rgba(236, 72, 153, 0.2);
  color: #f472b6;
}

.start-tag {
  background: rgba(16, 185, 129, 0.2);
  color: var(--accent-success);
}

.letters-row {
  display: flex;
  gap: 0.25rem;
}

.letter-tile {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 32px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 4px;
  font-family: var(--font-mono);
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-main);
  transition: var(--motion-interactive);
}

.letter-tile.changed-letter {
  background: linear-gradient(135deg, var(--accent-primary), #8b5cf6);
  border-color: #a5b4fc;
  color: #ffffff;
  transform: scale(1.08);
  box-shadow: 0 0 10px rgba(99, 102, 241, 0.4);
}
</style>
