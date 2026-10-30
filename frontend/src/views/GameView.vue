<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useGameStore } from '@/stores/game'
import ScoreBoard from '@/components/ScoreBoard.vue'
import Timer from '@/components/Timer.vue'
import WordChain from '@/components/WordChain.vue'
import Keyboard from '@/components/Keyboard.vue'
import HintBubble from '@/components/HintBubble.vue'

const router = useRouter()
const game = useGameStore()

const currentInput = ref('')
const showLifeLostToast = ref(false)

const wordLength = computed(() => game.wordLength || (game.currentWord ? game.currentWord.length : 4))

const inputLetters = computed(() => {
  const result = []
  const inputChars = currentInput.value.split('')
  for (let i = 0; i < wordLength.value; i++) {
    result.push(inputChars[i] || '')
  }
  return result
})

function handleKeyInput(char) {
  if (currentInput.value.length < wordLength.value) {
    currentInput.value += char
  }
}

function handleBackspace() {
  currentInput.value = currentInput.value.slice(0, -1)
}

async function handleSubmitWord() {
  if (currentInput.value.length !== wordLength.value) {
    game.triggerError(`Le mot doit comporter exactement ${wordLength.value} lettres`)
    return
  }

  const wordToPlay = currentInput.value
  const success = await game.playMove(wordToPlay)
  if (success) {
    currentInput.value = ''
  }
}

function handleSurrender() {
  if (confirm('Voulez-vous abandonner ce match ?')) {
    game.reset()
    router.push('/')
  }
}

// Watch for life lost event to display encouraging prompt
watch(
  () => game.lastEvent,
  (ev) => {
    if (ev && ev.includes('life_lost')) {
      showLifeLostToast.value = true
      setTimeout(() => {
        showLifeLostToast.value = false
      }, 3500)
    }
  }
)

// Route to ResultView as soon as finished is true
watch(
  () => game.finished,
  (isFinished) => {
    if (isFinished) {
      setTimeout(() => {
        router.push('/result')
      }, 800)
    }
  }
)

onMounted(() => {
  if (!game.matchId) {
    router.push('/')
  }
})
</script>

<template>
  <div class="game-view container" v-if="game.matchId">
    <!-- Top Bar -->
    <header class="game-header">
      <button type="button" class="btn-icon" title="Quitter" @click="handleSurrender">
        ✕
      </button>

      <div class="header-center">
        <span class="game-lang-badge">{{ game.lang.toUpperCase() }}</span>
        <span class="length-badge font-mono">{{ wordLength }} lettres</span>
      </div>

      <div class="header-right">
        <span class="mode-tag">{{ game.mode === 'solo' ? '🤖 VS IA' : '👥 DUO' }}</span>
      </div>
    </header>

    <!-- Score Board with 3 Hearts -->
    <ScoreBoard />

    <!-- Life Lost Encouraging Toast -->
    <div v-if="showLifeLostToast" class="life-lost-banner animate-pop">
      <span class="banner-icon heart-beat">💔</span>
      <div class="banner-content">
        <span class="banner-title">Oups, le temps est écoulé !</span>
        <span class="banner-sub">Pas d'inquiétude, réessaie ! Le chrono repart.</span>
      </div>
    </div>

    <!-- Gameplay Arena -->
    <div class="arena-layout">
      <!-- Ladder Word History -->
      <WordChain />

      <!-- Pedagogical Synonym Clue Component -->
      <HintBubble />

      <!-- Turn & Timer Section -->
      <div class="turn-section">
        <div class="turn-banner" :class="{ 'turn-ai': game.toMove === 1 && game.mode === 'solo' }">
          {{ game.currentPlayerLabel }}
        </div>
        <Timer />
      </div>

      <!-- Word Entry Slots -->
      <div class="input-card glass-panel" :class="{ 'animate-shake': game.shakeInput }">
        <div class="slots-label">
          Mot à transformer : <span class="current-word-highlight">{{ game.currentWord.toUpperCase() }}</span>
        </div>

        <div class="slots-container">
          <div
            v-for="(letter, idx) in inputLetters"
            :key="idx"
            class="input-slot"
            :class="{
              filled: letter !== '',
              active: currentInput.length === idx && game.isMyTurn
            }"
          >
            {{ letter.toUpperCase() }}
          </div>
        </div>

        <div v-if="game.errorMessage" class="error-text animate-shake">
          ⚠️ {{ game.errorMessage }}
        </div>
      </div>

      <!-- Virtual Keyboard -->
      <Keyboard
        :disabled="!game.isMyTurn || game.loading"
        @input-key="handleKeyInput"
        @backspace="handleBackspace"
        @submit="handleSubmitWord"
      />
    </div>
  </div>
</template>

<style scoped>
.game-view {
  max-width: 640px;
  display: flex;
  flex-direction: column;
  min-height: 95vh;
  justify-content: space-between;
}

.game-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.75rem;
}

.btn-icon {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-full);
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid var(--border-color);
  color: var(--text-muted);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-icon:hover {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
  border-color: rgba(239, 68, 68, 0.3);
}

.header-center {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.game-lang-badge {
  font-size: 0.8rem;
  font-weight: 800;
  padding: 0.2rem 0.55rem;
  background: var(--accent-primary);
  border-radius: var(--radius-sm);
  color: #fff;
}

.length-badge {
  font-size: 0.8rem;
  font-weight: 700;
  padding: 0.2rem 0.65rem;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-full);
  color: var(--accent-secondary);
}

.mode-tag {
  font-size: 0.75rem;
  font-weight: 700;
  padding: 0.25rem 0.65rem;
  border-radius: var(--radius-full);
  background: rgba(255, 255, 255, 0.08);
  color: var(--text-muted);
}

.life-lost-banner {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  padding: 0.75rem 1.1rem;
  background: rgba(244, 63, 94, 0.18);
  border: 1.5px solid var(--accent-danger);
  border-radius: var(--radius-md);
  margin-bottom: 0.85rem;
  box-shadow: 0 4px 15px rgba(244, 63, 94, 0.2);
}

.banner-icon {
  font-size: 1.6rem;
}

.banner-content {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
}

.banner-title {
  font-size: 0.95rem;
  font-weight: 800;
  color: #fff;
}

.banner-sub {
  font-size: 0.85rem;
  color: #fecdd3;
  font-weight: 500;
}

.arena-layout {
  display: flex;
  flex-direction: column;
}

.turn-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.75rem;
  padding: 0 0.5rem;
}

.turn-banner {
  font-size: 1.05rem;
  font-weight: 800;
  color: var(--accent-primary);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.turn-banner.turn-ai {
  color: #f472b6;
}

.input-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1.15rem 1rem;
  margin-bottom: 0.75rem;
}

.slots-label {
  font-size: 0.9rem;
  color: var(--text-muted);
  margin-bottom: 0.75rem;
}

.current-word-highlight {
  color: var(--accent-gold);
  font-family: var(--font-mono);
  font-weight: 800;
  letter-spacing: 0.1em;
  margin-left: 0.35rem;
}

.slots-container {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  flex-wrap: wrap;
  justify-content: center;
}

.input-slot {
  width: 52px;
  height: 60px;
  border-radius: var(--radius-md);
  border: 2px solid var(--border-color);
  background: rgba(255, 255, 255, 0.04);
  color: var(--text-main);
  font-family: var(--font-mono);
  font-size: 1.75rem;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 0 rgba(0, 0, 0, 0.3);
  transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
  user-select: none;
}

.input-slot.filled {
  border-color: var(--accent-primary);
  background: rgba(99, 102, 241, 0.12);
  box-shadow: 0 5px 0 var(--accent-primary-shadow);
  color: #fff;
  transform: translateY(-2px);
}

.input-slot.active {
  border-color: var(--accent-secondary);
  box-shadow: 0 0 14px rgba(6, 182, 212, 0.4);
}

.error-text {
  font-size: 0.85rem;
  color: #f43f5e;
  font-weight: 700;
  margin-top: 0.5rem;
}
</style>
