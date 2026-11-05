<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useGameStore } from '@/stores/game'

const game = useGameStore()
const timeLeft = ref(game.timeLimit)
let interval = null

const radius = 32
const circumference = 2 * Math.PI * radius

const strokeDashoffset = computed(() => {
  if (!game.timeLimit) return 0
  const progress = timeLeft.value / game.timeLimit
  return circumference * (1 - progress)
})

const timerColor = computed(() => {
  if (timeLeft.value <= 5) return 'var(--accent-danger)'
  if (timeLeft.value <= 15) return 'var(--accent-warning)'
  return 'var(--accent-primary)'
})

const isUrgent = computed(() => timeLeft.value <= 5 && !game.finished)

function startTimer() {
  stopTimer()
  timeLeft.value = game.timeLimit
  interval = setInterval(() => {
    if (game.finished) {
      stopTimer()
      return
    }
    if (timeLeft.value > 0) {
      timeLeft.value--
    } else {
      stopTimer()
      game.handleTimeout()
    }
  }, 1000)
}

function stopTimer() {
  if (interval) {
    clearInterval(interval)
    interval = null
  }
}

// Watch for turn changes or match resets
watch(
  () => [game.currentWord, game.toMove, game.part, game.finished, game.lives],
  ([,, , finished]) => {
    if (finished) {
      stopTimer()
    } else {
      startTimer()
    }
  }
)

onMounted(() => {
  if (!game.finished) {
    startTimer()
  }
})

onUnmounted(() => {
  stopTimer()
})
</script>

<template>
  <div
    class="timer-wrapper"
    :class="{ urgent: isUrgent }"
    role="timer"
    :aria-label="`Temps restant : ${timeLeft} secondes`"
  >
    <svg class="timer-svg" viewBox="0 0 80 80" aria-hidden="true">
      <circle
        class="timer-circle-bg"
        cx="40"
        cy="40"
        :r="radius"
      />
      <circle
        class="timer-circle-progress"
        cx="40"
        cy="40"
        :r="radius"
        :stroke="timerColor"
        :stroke-dasharray="circumference"
        :stroke-dashoffset="strokeDashoffset"
      />
    </svg>
    <div class="timer-number" :style="{ color: timerColor }">
      {{ timeLeft }}
    </div>
  </div>
</template>

<style scoped>
.timer-wrapper {
  position: relative;
  width: 76px;
  height: 76px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  transition: transform 0.2s ease;
}

@media (max-width: 600px) {
  .timer-wrapper {
    width: 64px;
    height: 64px;
  }

  .timer-number {
    font-size: 1.2rem;
  }
}

.timer-wrapper.urgent {
  animation: pulseTimer 0.6s infinite alternate;
}

@keyframes pulseTimer {
  from {
    transform: scale(1);
    filter: drop-shadow(0 0 5px rgba(239, 68, 68, 0.4));
  }
  to {
    transform: scale(1.1);
    filter: drop-shadow(0 0 15px rgba(239, 68, 68, 0.8));
  }
}

.timer-svg {
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}

.timer-circle-bg {
  fill: none;
  stroke: rgba(255, 255, 255, 0.08);
  stroke-width: 5;
}

.timer-circle-progress {
  fill: none;
  stroke-width: 5;
  stroke-linecap: round;
  transition: stroke-dashoffset 0.8s linear, stroke 0.3s ease;
}

.timer-number {
  position: absolute;
  font-family: var(--font-mono);
  font-size: 1.4rem;
  font-weight: 700;
  letter-spacing: -0.05em;
}
</style>
